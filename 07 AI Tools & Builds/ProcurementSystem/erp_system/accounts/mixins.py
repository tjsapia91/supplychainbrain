"""
Reusable permission mixins for all ERP views.

Usage in any module's views.py:
    from accounts.mixins import ProcurementRequiredMixin

    class MyView(ProcurementRequiredMixin, UpdateView):
        ...
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps


# ── Base mixin ────────────────────────────────────────────────────

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Base mixin: requires login + passes a role check.
    Subclasses override `allowed_roles` or `permission_method`.

    allowed_roles: tuple of Role values that can access the view
    permission_method: name of a User model method that returns bool
    """
    allowed_roles = ()
    permission_method = None
    raise_exception = True  # Return 403 instead of redirect

    def test_func(self):
        user = self.request.user
        if user.is_admin_user:
            return True
        if self.permission_method:
            method = getattr(user, self.permission_method, None)
            if method and callable(method):
                return method()
        if self.allowed_roles:
            return user.role in self.allowed_roles
        return False


# ── Concrete mixins (one per module / permission level) ───────────

class AdminRequiredMixin(RoleRequiredMixin):
    """Only admin / superuser."""
    def test_func(self):
        return self.request.user.is_admin_user


class ProcurementRequiredMixin(RoleRequiredMixin):
    """Can create/edit PPOs and purchase requests."""
    permission_method = 'can_create_ppo'


class ApprovalRequiredMixin(RoleRequiredMixin):
    """Can approve purchase requests."""
    permission_method = 'can_approve_pr'


class ReceivingRequiredMixin(RoleRequiredMixin):
    """Can create/edit goods receipts."""
    permission_method = 'can_receive_goods'


class FinanceRequiredMixin(RoleRequiredMixin):
    """Can manage AP invoices."""
    permission_method = 'can_manage_invoices'


class InventoryRequiredMixin(RoleRequiredMixin):
    """Can manage inventory and stock movements."""
    permission_method = 'can_manage_inventory'


class ContainerRequiredMixin(RoleRequiredMixin):
    """Can manage container plans."""
    permission_method = 'can_manage_containers'


class LandedCostRequiredMixin(RoleRequiredMixin):
    """Can manage landed cost documents."""
    permission_method = 'can_manage_landed_costs'


class VendorRequiredMixin(RoleRequiredMixin):
    """Can manage vendor records."""
    permission_method = 'can_manage_vendors'


class ViewerOrAboveMixin(RoleRequiredMixin):
    """Any authenticated user with any role can view (read-only views)."""
    def test_func(self):
        return self.request.user.is_authenticated


# ── Function-based view decorators ────────────────────────────────

def role_required(*roles):
    """
    Decorator for function-based views.

    Usage:
        @login_required
        @role_required('admin', 'supply_chain_manager')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_admin_user or user.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('You do not have permission to access this page.')
        return wrapper
    return decorator


def permission_check(method_name):
    """
    Decorator that calls a User model permission method.

    Usage:
        @login_required
        @permission_check('can_create_ppo')
        def create_ppo(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            method = getattr(user, method_name, None)
            if method and callable(method) and method():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('You do not have permission to perform this action.')
        return wrapper
    return decorator
