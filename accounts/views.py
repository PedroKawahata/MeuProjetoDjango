from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass  # o destino vem do LOGOUT_REDIRECT_URL, no settings.py


class UserCreateView(CreateView):
    template_name = "accounts/user_form_create.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")