from django.conf import settings


def site_info(request):
    return {
        'site_name': 'Michael Todd Beauty ERP',
        'site_description': 'Procurement System',
    }
