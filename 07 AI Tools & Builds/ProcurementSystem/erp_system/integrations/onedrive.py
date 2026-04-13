"""
OneDrive integration for MTB ERP.
Handles OAuth token management, file uploads, and folder creation via Microsoft Graph API.
"""
import os
import json
import time
import logging
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

# ─── Configuration ───────────────────────────────────────────────────────────
CLIENT_ID = os.environ.get('ONEDRIVE_CLIENT_ID', '0d90f2af-31fa-4a0b-a547-ebcb14f1dba6')
CLIENT_SECRET = os.environ.get('ONEDRIVE_CLIENT_SECRET', '')
REDIRECT_URI = os.environ.get('ONEDRIVE_REDIRECT_URI', 'https://tjs91.pythonanywhere.com/oauth/callback/')
TOKEN_FILE = os.environ.get('ONEDRIVE_TOKEN_FILE', os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'onedrive_token.json'
))

# Microsoft endpoints (consumers = personal accounts)
AUTHORITY = 'https://login.microsoftonline.com/consumers'
TOKEN_URL = f'{AUTHORITY}/oauth2/v2.0/token'
AUTH_URL = f'{AUTHORITY}/oauth2/v2.0/authorize'
GRAPH_BASE = 'https://graph.microsoft.com/v1.0'

SCOPES = 'Files.ReadWrite offline_access User.Read'

# ─── Root folder in OneDrive ─────────────────────────────────────────────────
ONEDRIVE_ROOT = os.environ.get('ONEDRIVE_ROOT_FOLDER', 'Michael Todd Beauty')


# ─── Token Management ────────────────────────────────────────────────────────

def _load_token():
    """Load stored token from disk."""
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _save_token(token_data):
    """Persist token to disk."""
    token_data['saved_at'] = time.time()
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    logger.info('OneDrive token saved.')


def _token_expired(token_data):
    """Check if the access token is expired (with 5-min buffer)."""
    if not token_data or 'saved_at' not in token_data:
        return True
    expires_in = token_data.get('expires_in', 3600)
    return time.time() > (token_data['saved_at'] + expires_in - 300)


def get_access_token():
    """
    Return a valid access token, refreshing if needed.
    Returns None if no token is available (user needs to authorize).
    """
    token_data = _load_token()
    if not token_data:
        logger.warning('No OneDrive token found. User must authorize.')
        return None

    if not _token_expired(token_data):
        return token_data['access_token']

    # Refresh the token
    refresh_token = token_data.get('refresh_token')
    if not refresh_token:
        logger.warning('No refresh token available. User must re-authorize.')
        return None

    try:
        resp = requests.post(TOKEN_URL, data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'scope': SCOPES,
        }, timeout=15)
        resp.raise_for_status()
        new_token = resp.json()
        _save_token(new_token)
        logger.info('OneDrive token refreshed successfully.')
        return new_token['access_token']
    except Exception as e:
        logger.error(f'Failed to refresh OneDrive token: {e}')
        return None


def exchange_code_for_token(auth_code):
    """
    Exchange an authorization code for access + refresh tokens.
    Called from the OAuth callback view.
    """
    resp = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
    }, timeout=15)
    resp.raise_for_status()
    token_data = resp.json()
    _save_token(token_data)
    return token_data


def get_auth_url():
    """Build the Microsoft OAuth authorization URL."""
    params = (
        f'client_id={CLIENT_ID}'
        f'&response_type=code'
        f'&redirect_uri={REDIRECT_URI}'
        f'&response_mode=query'
        f'&scope={SCOPES.replace(" ", "%20")}'
    )
    return f'{AUTH_URL}?{params}'


def is_connected():
    """Quick check: do we have a valid (or refreshable) token?"""
    token_data = _load_token()
    if not token_data:
        return False
    if not _token_expired(token_data):
        return True
    return token_data.get('refresh_token') is not None


# ─── Graph API Helpers ───────────────────────────────────────────────────────

def _headers():
    """Return auth headers for Graph API calls."""
    token = get_access_token()
    if not token:
        raise ConnectionError('No valid OneDrive access token.')
    return {'Authorization': f'Bearer {token}'}


def _ensure_folder(folder_path):
    """
    Ensure a folder path exists under ONEDRIVE_ROOT, creating segments as needed.
    folder_path: relative path like 'Purchase Orders/PPO-3150'
    Returns the folder's driveItem ID.
    """
    full_path = f'{ONEDRIVE_ROOT}/{folder_path}'.strip('/')
    segments = full_path.split('/')
    parent_id = None  # start at root

    for segment in segments:
        if parent_id:
            url = f'{GRAPH_BASE}/me/drive/items/{parent_id}/children'
        else:
            url = f'{GRAPH_BASE}/me/drive/root/children'

        # Check if folder exists
        resp = requests.get(url, headers=_headers(), params={
            '$filter': f"name eq '{segment}'",
            '$select': 'id,name,folder',
        }, timeout=15)
        resp.raise_for_status()
        items = resp.json().get('value', [])

        folder_item = None
        for item in items:
            if item['name'].lower() == segment.lower() and 'folder' in item:
                folder_item = item
                break

        if folder_item:
            parent_id = folder_item['id']
        else:
            # Create the folder
            if parent_id:
                create_url = f'{GRAPH_BASE}/me/drive/items/{parent_id}/children'
            else:
                create_url = f'{GRAPH_BASE}/me/drive/root/children'

            create_resp = requests.post(create_url, headers={
                **_headers(),
                'Content-Type': 'application/json',
            }, json={
                'name': segment,
                'folder': {},
                '@microsoft.graph.conflictBehavior': 'fail',
            }, timeout=15)
            create_resp.raise_for_status()
            parent_id = create_resp.json()['id']
            logger.info(f'Created OneDrive folder: {segment}')

    return parent_id


def upload_file(folder_path, filename, file_content, content_type='application/octet-stream'):
    """
    Upload a file to OneDrive.
    folder_path: relative to ONEDRIVE_ROOT (e.g., 'Purchase Orders/PPO-3150')
    filename: the target filename
    file_content: bytes or file-like object
    Returns: driveItem dict from Graph API
    """
    try:
        folder_id = _ensure_folder(folder_path)

        # For files under 4MB, use simple upload
        if isinstance(file_content, bytes):
            size = len(file_content)
        else:
            file_content.seek(0, 2)
            size = file_content.tell()
            file_content.seek(0)

        if size < 4 * 1024 * 1024:
            # Simple upload
            url = f'{GRAPH_BASE}/me/drive/items/{folder_id}:/{filename}:/content'
            resp = requests.put(url, headers={
                **_headers(),
                'Content-Type': content_type,
            }, data=file_content if isinstance(file_content, bytes) else file_content.read(),
            timeout=30)
            resp.raise_for_status()
            logger.info(f'Uploaded {filename} to OneDrive: {folder_path}/')
            return resp.json()
        else:
            # Large file upload session
            return _upload_large_file(folder_id, filename, file_content, size)

    except Exception as e:
        logger.error(f'OneDrive upload failed for {filename}: {e}')
        raise


def _upload_large_file(folder_id, filename, file_content, total_size):
    """Upload files > 4MB using upload sessions."""
    # Create upload session
    url = f'{GRAPH_BASE}/me/drive/items/{folder_id}:/{filename}:/createUploadSession'
    resp = requests.post(url, headers={
        **_headers(),
        'Content-Type': 'application/json',
    }, json={
        'item': {
            '@microsoft.graph.conflictBehavior': 'replace',
            'name': filename,
        }
    }, timeout=15)
    resp.raise_for_status()
    upload_url = resp.json()['uploadUrl']

    # Upload in 5MB chunks
    chunk_size = 5 * 1024 * 1024
    offset = 0

    if isinstance(file_content, bytes):
        data = file_content
    else:
        data = file_content.read()

    while offset < total_size:
        end = min(offset + chunk_size, total_size)
        chunk = data[offset:end]
        content_range = f'bytes {offset}-{end - 1}/{total_size}'

        chunk_resp = requests.put(upload_url, headers={
            'Content-Length': str(len(chunk)),
            'Content-Range': content_range,
        }, data=chunk, timeout=60)

        if chunk_resp.status_code in (200, 201):
            logger.info(f'Upload complete: {filename}')
            return chunk_resp.json()
        elif chunk_resp.status_code == 202:
            offset = end
            continue
        else:
            chunk_resp.raise_for_status()

    raise Exception('Upload session ended without completion')


# ─── ERP-Specific Sync Functions ─────────────────────────────────────────────

def sync_ppo_attachment(ppo_number, filename, file_content, content_type='application/octet-stream'):
    """Upload a PPO attachment to Purchase Orders/PPO-{number}/"""
    folder = f'Purchase Orders/PPO-{ppo_number}'
    return upload_file(folder, filename, file_content, content_type)


def sync_proforma_invoice(ppo_number, filename, file_content, content_type='application/pdf'):
    """Upload a proforma invoice to Purchase Orders/PPO-{number}/"""
    folder = f'Purchase Orders/PPO-{ppo_number}'
    return upload_file(folder, filename, file_content, content_type)


def sync_ppo_pdf(ppo_number, filename, file_content, content_type='application/pdf'):
    """Upload a generated PPO PDF to Purchase Orders/PPO-{number}/"""
    folder = f'Purchase Orders/PPO-{ppo_number}'
    return upload_file(folder, filename, file_content, content_type)


def sync_shipping_doc(container_name, doc_type, filename, file_content, content_type='application/octet-stream'):
    """Upload a shipping doc to Containers/{container}/{doc_type}/"""
    folder = f'Containers/{container_name}'
    # Prefix filename with doc type for clarity
    prefixed_name = f'{doc_type}_{filename}' if not filename.startswith(doc_type) else filename
    return upload_file(folder, prefixed_name, file_content, content_type)


def sync_goods_receipt(grpo_number, filename, file_content, content_type='application/pdf'):
    """Upload a goods receipt to Goods Receipts/"""
    folder = 'Goods Receipts'
    return upload_file(folder, filename, file_content, content_type)


def sync_intransit_log_backup(fiscal_year, filename, file_content, content_type='text/csv'):
    """Upload an in-transit log backup to Backups/InTransitLog/FY{year}/"""
    folder = f'Backups/InTransitLog/FY{fiscal_year}'
    return upload_file(folder, filename, file_content, content_type)
