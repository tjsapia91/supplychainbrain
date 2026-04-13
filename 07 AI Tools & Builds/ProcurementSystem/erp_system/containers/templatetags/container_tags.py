from django import template

register = template.Library()


@register.filter
def status_badge(status):
    """Return Bootstrap badge class for container status"""
    colors = {
        'planning': 'bg-secondary',
        'packing': 'bg-info',
        'booked': 'bg-primary',
        'ready_to_load': 'bg-warning text-dark',
        'loaded': 'bg-primary',
        'in_transit': 'bg-info',
        'at_port': 'bg-warning text-dark',
        'customs': 'bg-warning text-dark',
        'delivered': 'bg-success',
        'completed': 'bg-success',
        'cancelled': 'bg-danger',
    }
    return colors.get(status, 'bg-secondary')


@register.filter
def utilization_color(pct):
    """Return color class based on utilization percentage"""
    try:
        pct = float(pct)
    except (TypeError, ValueError):
        return 'bg-secondary'
    if pct >= 95:
        return 'bg-success'
    elif pct >= 75:
        return 'bg-info'
    elif pct >= 50:
        return 'bg-warning'
    else:
        return 'bg-danger'


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (TypeError, ValueError):
        return 0


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0
