from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'department', 'phone'),
        }),
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        ('ERP Info', {'fields': ('role', 'phone', 'department')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_editable = ('is_active',)

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected users')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected users')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
