"""
OAuth callback view for OneDrive integration.
"""
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from integrations.onedrive import exchange_code_for_token, get_auth_url, is_connected

logger = logging.getLogger(__name__)


def oauth_callback(request):
    """
    Handle the OAuth redirect from Microsoft.
    Exchanges the auth code for access + refresh tokens.
    """
    error = request.GET.get('error')
    if error:
        error_desc = request.GET.get('error_description', 'Unknown error')
        logger.error(f'OAuth error: {error} - {error_desc}')
        return HttpResponse(
            f'<h2>OneDrive Authorization Failed</h2>'
            f'<p>Error: {error}</p>'
            f'<p>{error_desc}</p>'
            f'<p><a href="/oauth/connect/">Try again</a></p>',
            status=400
        )

    code = request.GET.get('code')
    if not code:
        return HttpResponse(
            '<h2>Missing authorization code</h2>'
            '<p><a href="/oauth/connect/">Try again</a></p>',
            status=400
        )

    try:
        token_data = exchange_code_for_token(code)
        logger.info('OneDrive authorization successful.')
        return HttpResponse(
            '<h2>OneDrive Connected Successfully!</h2>'
            '<p>The ERP system is now connected to OneDrive.</p>'
            '<p>Files will be automatically synced when uploaded.</p>'
            '<p><a href="/">Return to Dashboard</a></p>'
        )
    except Exception as e:
        logger.error(f'Token exchange failed: {e}')
        return HttpResponse(
            f'<h2>Token Exchange Failed</h2>'
            f'<p>Error: {str(e)}</p>'
            f'<p><a href="/oauth/connect/">Try again</a></p>',
            status=500
        )


@staff_member_required
def oauth_connect(request):
    """Redirect staff to Microsoft's authorization page."""
    if is_connected():
        return HttpResponse(
            '<h2>OneDrive Already Connected</h2>'
            '<p>The ERP is already connected to OneDrive.</p>'
            '<p><a href="/oauth/connect/?force=1">Re-authorize</a> | '
            '<a href="/">Dashboard</a></p>'
        )
    return HttpResponseRedirect(get_auth_url())


@staff_member_required
def oauth_status(request):
    """Quick status check for OneDrive connection."""
    connected = is_connected()
    return HttpResponse(
        f'<h2>OneDrive Status</h2>'
        f'<p>Connected: <strong>{"Yes" if connected else "No"}</strong></p>'
        f'{"" if connected else "<p><a href=/oauth/connect/>Connect Now</a></p>"}'
        f'<p><a href="/">Dashboard</a></p>'
    )
