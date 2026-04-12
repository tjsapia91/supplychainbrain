from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """Form for creating new users with proper password validation."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Must meet complexity requirements (8+ chars, not too common, etc.).',
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Run Django's AUTH_PASSWORD_VALIDATORS
        validate_password(password)
        return password

    def clean_password2(self):
        cd = self.cleaned_data
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for editing existing users (no password field — use separate change flow)."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'department', 'phone', 'is_active')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_role(self):
        """Prevent non-admins from escalating to admin."""
        role = self.cleaned_data.get('role')
        if role == User.Role.ADMIN and not self.current_user_is_admin:
            raise forms.ValidationError('Only administrators can assign the admin role.')
        return role
