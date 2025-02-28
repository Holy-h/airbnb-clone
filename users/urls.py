from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path(
        "verify/<str:secret>/",
        views.complete_verification,
        name="complete-verification",
    ),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path(
        "update-Password/", views.UpdatePasswordView.as_view(), name="update-password"
    ),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
    path("switch_language/", views.switch_language, name="switch_language"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
]
