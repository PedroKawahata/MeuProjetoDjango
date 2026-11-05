from django.urls import path
from accounts.views import UserLoginView, UserLogoutView, UserCreateView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("cadastro/", UserCreateView.as_view(), name="register"),
]