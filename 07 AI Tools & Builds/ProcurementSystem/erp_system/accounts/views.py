from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.views.generic.edit import FormView

from .forms import UserCreationForm, UserUpdateForm
from .mixins import AdminRequiredMixin

User = get_user_model()


# ── Auth views ────────────────────────────────────────────────────

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('login')


# ── Password change (any logged-in user) ─────────────────────────

class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Password updated successfully.')
        return super().form_valid(form)


# ── Profile (own user) ───────────────────────────────────────────

class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user


# ── Admin: user management ────────────────────────────────────────

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.all().order_by('last_name', 'first_name')
        role = self.request.GET.get('role')
        search = self.request.GET.get('q')
        if role:
            qs = qs.filter(role=role)
        if search:
            qs = qs.filter(
                models_Q(username__icontains=search)
                | models_Q(first_name__icontains=search)
                | models_Q(last_name__icontains=search)
                | models_Q(email__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['roles'] = User.Role.choices
        ctx['current_role'] = self.request.GET.get('role', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'User "{form.cleaned_data["username"]}" created.')
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.current_user_is_admin = self.request.user.is_admin_user
        return form

    def form_valid(self, form):
        messages.success(self.request, f'User "{self.object.username}" updated.')
        return super().form_valid(form)


# ── helper ────────────────────────────────────────────────────────
from django.db.models import Q as models_Q  # noqa: E402
