"""
Email service for sending PPOs and notifications via Microsoft 365 (Graph API).

Setup instructions:
1. Register an app in Azure AD (see Azure_Email_Setup_Guide.md)
2. Add credentials to erp/settings.py or a .env file
3. Install: pip install msal requests python-dotenv

This module provides:
- send_ppo_to_vendor()      — Single PPO email to vendor
- batch_send_ppos()         — Multiple PPOs in one email per vendor
- send_ceo_approval_request() — Notify CEO that a PPO needs approval
- send_status_notification()  — Generic status change notification
"""

import logging
import base64
import os
from io import BytesIO
from django.conf import settings

logger = logging.getLogger(__name__)


# ============================================================================
# SENDER CONFIGURATION
# ============================================================================

# Authorized senders — the dropdown in batch send / single send
AUTHORIZED_SENDERS = {
    'tom': {
        'name': 'Tom Sapia',
        'email': 'tom@michaeltoddbeauty.com',
    },
    'augusto': {
        'name': 'Augusto',
        'email': 'augusto@michaeltoddbeauty.com',
    },
    'donna': {
        'name': 'Donna',
        'email': 'donna@michaeltoddbeauty.com',
    },
}

CC_RECIPIENTS = [
    'supplychain@michaeltoddbeauty.com',
]


def get_sender_choices():
    """Return choices for Django form field."""
    return [(key, f"{val['name']} ({val['email']})") for key, val in AUTHORIZED_SENDERS.items()]


# ============================================================================
# MICROSOFT GRAPH API CLIENT
# ============================================================================

def _get_graph_token():
    """
    Acquire an access token for Microsoft Graph API using client credentials flow.
    Requires: AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET in settings.
    """
    try:
        import msal
    except ImportError:
        logger.error("msal package not installed. Run: pip install msal")
        return None

    tenant_id = getattr(settings, 'AZURE_TENANT_ID', '')
    client_id = getattr(settings, 'AZURE_CLIENT_ID', '')
    client_secret = getattr(settings, 'AZURE_CLIENT_SECRET', '')

    if not all([tenant_id, client_id, client_secret]):
        logger.warning("Azure credentials not configured in settings. Email sending disabled.")
        return None

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if "access_token" in result:
        return result["access_token"]
    else:
        logger.error(f"Failed to acquire token: {result.get('error_description', 'Unknown error')}")
        return None


def _send_via_graph(sender_email, to_emails, cc_emails, subject, body_html, attachments=None):
    """
    Send an email via Microsoft Graph API.

    Args:
        sender_email: str — the From address (must be an authorized mailbox)
        to_emails: list of str — recipient email addresses
        cc_emails: list of str — CC email addresses
        subject: str — email subject
        body_html: str — HTML email body
        attachments: list of dicts — [{'name': 'file.pdf', 'content_bytes': b'...', 'content_type': 'application/pdf'}]

    Returns:
        bool — True if sent successfully
    """
    import requests

    token = _get_graph_token()
    if not token:
        logger.warning("No Graph API token — email not sent (credentials not configured)")
        return False

    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body_html,
            },
            "from": {
                "emailAddress": {"address": sender_email}
            },
            "toRecipients": [
                {"emailAddress": {"address": email}} for email in to_emails
            ],
            "ccRecipients": [
                {"emailAddress": {"address": email}} for email in cc_emails
            ],
        },
        "saveToSentItems": True,
    }

    # Add attachments
    if attachments:
        message["message"]["attachments"] = []
        for att in attachments:
            message["message"]["attachments"].append({
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": att["name"],
                "contentType": att.get("content_type", "application/pdf"),
                "contentBytes": base64.b64encode(att["content_bytes"]).decode("utf-8"),
            })

    url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=message)

    if response.status_code == 202:
        logger.info(f"Email sent successfully from {sender_email} to {to_emails}")
        return True
    else:
        logger.error(f"Email send failed: {response.status_code} — {response.text}")
        return False


# ============================================================================
# HIGH-LEVEL EMAIL FUNCTIONS
# ============================================================================

def send_ppo_to_vendor(ppo, sender_key, message_text=''):
    """
    Send a single PPO to the vendor via email.

    Args:
        ppo: PlannedPurchaseOrder instance
        sender_key: str — key from AUTHORIZED_SENDERS (e.g. 'tom')
        message_text: str — optional message to include in email body
    """
    sender = AUTHORIZED_SENDERS.get(sender_key)
    if not sender:
        logger.error(f"Unknown sender key: {sender_key}")
        return False

    vendor = ppo.vendor
    to_emails = [vendor.contact_email] if vendor.contact_email else []

    if not to_emails:
        logger.warning(f"No contact email for vendor {vendor.name} — cannot send PPO-{ppo.ppo_number}")
        return False

    subject = f"Purchase Order from Michael Todd Beauty — PPO-{ppo.ppo_number}"

    body_html = _build_ppo_email_body([ppo], sender, message_text)

    # Generate PDF attachment
    attachments = _generate_ppo_attachments([ppo])

    return _send_via_graph(
        sender_email=sender['email'],
        to_emails=to_emails,
        cc_emails=CC_RECIPIENTS,
        subject=subject,
        body_html=body_html,
        attachments=attachments,
    )


def batch_send_ppos(ppos, sender_key, message_text=''):
    """
    Batch send multiple PPOs grouped by vendor. One email per vendor.

    Args:
        ppos: queryset or list of PlannedPurchaseOrder instances
        sender_key: str — key from AUTHORIZED_SENDERS
        message_text: str — optional message

    Returns:
        dict — {'sent': count, 'failed': count, 'errors': [str]}
    """
    from itertools import groupby
    from operator import attrgetter

    sender = AUTHORIZED_SENDERS.get(sender_key)
    if not sender:
        return {'sent': 0, 'failed': 0, 'errors': [f'Unknown sender: {sender_key}']}

    results = {'sent': 0, 'failed': 0, 'errors': []}

    # Group by vendor
    sorted_ppos = sorted(ppos, key=attrgetter('vendor_id'))
    for vendor_id, group in groupby(sorted_ppos, key=attrgetter('vendor_id')):
        vendor_ppos = list(group)
        vendor = vendor_ppos[0].vendor

        to_emails = [vendor.contact_email] if vendor.contact_email else []
        if not to_emails:
            results['errors'].append(f"No email for {vendor.name} — skipped {len(vendor_ppos)} PPOs")
            results['failed'] += len(vendor_ppos)
            continue

        ppo_numbers = ', '.join(f'PPO-{p.ppo_number}' for p in vendor_ppos)
        subject = f"Purchase Order{'s' if len(vendor_ppos) > 1 else ''} from Michael Todd Beauty — {ppo_numbers}"

        body_html = _build_ppo_email_body(vendor_ppos, sender, message_text)
        attachments = _generate_ppo_attachments(vendor_ppos)

        success = _send_via_graph(
            sender_email=sender['email'],
            to_emails=to_emails,
            cc_emails=CC_RECIPIENTS,
            subject=subject,
            body_html=body_html,
            attachments=attachments,
        )

        if success:
            results['sent'] += len(vendor_ppos)
        else:
            results['failed'] += len(vendor_ppos)
            results['errors'].append(f"Failed to send to {vendor.name} ({vendor.contact_email})")

    return results


def send_ceo_approval_request(ppo, requester_name=''):
    """Send notification to CEO that a PPO needs approval."""
    ceo_email = getattr(settings, 'CEO_EMAIL', '')
    if not ceo_email:
        logger.warning("CEO_EMAIL not configured in settings")
        return False

    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    approval_url = f"{site_url}/procurement/ppos/{ppo.pk}/ceo-approve/"

    subject = f"Approval Required: PPO-{ppo.ppo_number} — {ppo.vendor.name}"

    body_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #1f4788; color: white; padding: 20px 30px; border-radius: 8px 8px 0 0;">
            <h2 style="margin: 0; font-size: 1.25rem;">CEO Approval Required</h2>
        </div>
        <div style="padding: 30px; background: #f8f9fa; border: 1px solid #e9ecef; border-top: none; border-radius: 0 0 8px 8px;">
            <p>A purchase order requires your review and approval:</p>
            <table style="width: 100%; margin: 20px 0;">
                <tr><td style="padding: 8px 0; font-weight: 600; color: #555;">PPO Number:</td><td style="padding: 8px 0;">PPO-{ppo.ppo_number}</td></tr>
                <tr><td style="padding: 8px 0; font-weight: 600; color: #555;">Vendor:</td><td style="padding: 8px 0;">{ppo.vendor.name}</td></tr>
                <tr><td style="padding: 8px 0; font-weight: 600; color: #555;">Total:</td><td style="padding: 8px 0;">${ppo.total:,.2f}</td></tr>
                <tr><td style="padding: 8px 0; font-weight: 600; color: #555;">Requested By:</td><td style="padding: 8px 0;">{requester_name}</td></tr>
            </table>
            <a href="{approval_url}" style="display: inline-block; background: #1f4788; color: white; padding: 12px 32px; border-radius: 6px; text-decoration: none; font-weight: 600;">Review & Approve</a>
            <p style="margin-top: 20px; font-size: 0.85rem; color: #6c757d;">Click the button above to review, approve, or reject this purchase order.</p>
        </div>
    </div>
    """

    # Use first available sender (or a dedicated system sender)
    sender_email = CC_RECIPIENTS[0] if CC_RECIPIENTS else 'noreply@michaeltoddbeauty.com'

    return _send_via_graph(
        sender_email=sender_email,
        to_emails=[ceo_email],
        cc_emails=[],
        subject=subject,
        body_html=body_html,
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _build_ppo_email_body(ppos, sender, message_text=''):
    """Build the HTML email body for PPO vendor emails."""
    ppo_list_html = ''
    for ppo in ppos:
        line_count = ppo.lines.count()
        ppo_list_html += f"""
        <tr>
            <td style="padding: 10px 15px; border-bottom: 1px solid #eee; font-weight: 600;">PPO-{ppo.ppo_number}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #eee;">{ppo.date.strftime('%B %d, %Y') if ppo.date else '—'}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #eee;">{line_count} item{'s' if line_count != 1 else ''}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #eee; text-align: right;">${ppo.total:,.2f}</td>
        </tr>
        """

    message_section = ''
    if message_text:
        message_section = f"""
        <div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 6px; padding: 15px; margin: 20px 0;">
            <strong>Message from {sender['name']}:</strong>
            <p style="margin: 8px 0 0 0;">{message_text}</p>
        </div>
        """

    vendor_name = ppos[0].vendor.name if ppos else 'Vendor'

    body_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 650px; margin: 0 auto;">
        <div style="background: #1f4788; color: white; padding: 20px 30px; border-radius: 8px 8px 0 0;">
            <h2 style="margin: 0; font-size: 1.25rem;">Purchase Order{'s' if len(ppos) > 1 else ''} from Michael Todd Beauty</h2>
        </div>
        <div style="padding: 30px; background: white; border: 1px solid #e9ecef; border-top: none; border-radius: 0 0 8px 8px;">
            <p>Dear {vendor_name},</p>
            <p>Please find the attached purchase order{'s' if len(ppos) > 1 else ''} for your review and confirmation.</p>

            {message_section}

            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background: #f8f9fa;">
                        <th style="padding: 10px 15px; text-align: left; font-size: 0.85rem; color: #555; border-bottom: 2px solid #d4a574;">PO #</th>
                        <th style="padding: 10px 15px; text-align: left; font-size: 0.85rem; color: #555; border-bottom: 2px solid #d4a574;">Date</th>
                        <th style="padding: 10px 15px; text-align: left; font-size: 0.85rem; color: #555; border-bottom: 2px solid #d4a574;">Items</th>
                        <th style="padding: 10px 15px; text-align: right; font-size: 0.85rem; color: #555; border-bottom: 2px solid #d4a574;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {ppo_list_html}
                </tbody>
            </table>

            <p>Please review the attached PDF{'s' if len(ppos) > 1 else ''} and confirm the order{'s' if len(ppos) > 1 else ''} at your earliest convenience.</p>

            <hr style="border: none; border-top: 1px solid #e9ecef; margin: 25px 0;">
            <p style="font-size: 0.85rem; color: #6c757d;">
                Best regards,<br>
                <strong>{sender['name']}</strong><br>
                Michael Todd Beauty<br>
                584 NW University Blvd., Suite 600<br>
                Port St. Lucie, FL 34986<br>
                supplychain@michaeltoddbeauty.com
            </p>
        </div>
    </div>
    """
    return body_html


def _generate_ppo_attachments(ppos):
    """Generate PDF attachments for the given PPOs."""
    attachments = []
    try:
        from .pdf_generator import generate_ppo_pdf
        for ppo in ppos:
            pdf_bytes = generate_ppo_pdf(ppo)
            if pdf_bytes:
                # generate_ppo_pdf returns an HttpResponse — extract the content
                if hasattr(pdf_bytes, 'content'):
                    content = pdf_bytes.content
                elif isinstance(pdf_bytes, bytes):
                    content = pdf_bytes
                else:
                    content = pdf_bytes
                attachments.append({
                    'name': f'PPO-{ppo.ppo_number}.pdf',
                    'content_bytes': content,
                    'content_type': 'application/pdf',
                })
    except Exception as e:
        logger.error(f"Failed to generate PDF attachments: {e}")

    return attachments


def is_email_configured():
    """Check if Azure email credentials are configured."""
    return all([
        getattr(settings, 'AZURE_TENANT_ID', ''),
        getattr(settings, 'AZURE_CLIENT_ID', ''),
        getattr(settings, 'AZURE_CLIENT_SECRET', ''),
    ])
