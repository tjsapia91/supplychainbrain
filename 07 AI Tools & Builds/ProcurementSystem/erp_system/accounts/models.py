from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        SUPPLY_CHAIN_MANAGER = 'supply_chain_manager', 'Supply Chain Manager'
        BUYER = 'buyer', 'Buyer'
        WAREHOUSE = 'warehouse', 'Warehouse Staff'
        FINANCE = 'finance', 'Finance/AP'
        VIEWER = 'viewer', 'Viewer'

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.VIEWER,
        db_index=True,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Enter a valid phone number (9-15 digits, optional + prefix).',
            )
        ],
    )
    department = models.CharField(max_length=100, blank=True, db_index=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        full = self.get_full_name()
        return f"{full} ({self.get_role_display()})" if full else self.username

    # ── role helpers ──────────────────────────────────────────────
    @property
    def is_admin_user(self):
        """True for admins and superusers."""
        return self.role == self.Role.ADMIN or self.is_superuser

    def has_role(self, *roles):
        """Check if user has any of the given roles (admin always passes)."""
        if self.is_admin_user:
            return True
        return self.role in roles

    # ── permission helpers (used by mixins & views) ───────────────
    def can_create_ppo(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.BUYER)

    def can_approve_pr(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER)

    def can_receive_goods(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.WAREHOUSE)

    def can_manage_invoices(self):
        return self.has_role(self.Role.FINANCE)

    def can_manage_inventory(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.WAREHOUSE)

    def can_manage_containers(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.BUYER)

    def can_manage_landed_costs(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.FINANCE)

    def can_manage_vendors(self):
        return self.has_role(self.Role.SUPPLY_CHAIN_MANAGER, self.Role.BUYER)
