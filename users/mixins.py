from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse


class EmailLoginOnlyView(UserPassesTestMixin):
    """ login_method: email """

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "⛔ Email로 로그인한 이용자만 비밀번호를 변경할 수 있어요.")
        return redirect(reverse("core:home"))


class LoggedOutOnlyView(UserPassesTestMixin):
    """ 로그인하지 않은 유저만 접근 가능 """

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "⛔ 접근할 수 없는 페이지입니다.")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    """
    로그인한 유저만 접근 가능
    """

    login_url = reverse_lazy("users:login")
    # permission_denied_message = "⛔ 로그인이 필요한 페이지입니다."
