from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class LoggedOutOnlyView(UserPassesTestMixin):
    """ LoggedOutOnlyView Definition """

    permission_denied_message = "😰😰페이지를 찾을 수 없어요."

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("core:home"))
