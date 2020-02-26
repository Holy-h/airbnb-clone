import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    """ LoginView Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            # to do - email_verified=False일 때, 인증 추가
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        messages.info(self.request, f"{self.request.user.first_name}님, 반가워요! 🤭")
        if next_arg is None:
            return reverse("core:home")
        return next_arg


def log_out(request):
    messages.info(request, f"{request.user.first_name}님, 다음에 또 만나요! 🤗")
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(mixins.LoggedOutOnlyView, FormView):

    """ SignupView Definition """

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # form이 유효하면 save()
        form.save()

        # save() 이후에 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            # to do - 이메일 인증 다른 방식으로 진행하기
            # user.verify_email()
        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    """ GithubException Definition """

    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is None:
            raise GithubException("🤔🤔Github 코드를 받을 수 없어요.")
        token_request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise GithubException("😱😱Github 인증 토큰을 받을 수 없어요.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        # api 요청 성공 여부 파악 status_code or resultData
        profile_json = profile_request.json()
        username = profile_json.get("login", None)
        if username is None:
            raise GithubException("😟😟Github 프로필에서 필요한 정보를 얻을 수 없어요.")
        # 필요한 UserData 담기
        name = profile_json.get("name")
        email = profile_json.get("email")
        bio = profile_json.get("bio")
        # to do: name, email, bio가 None인 경우
        # 기존에 가입한 유저가 있는지 확인
        try:
            # 이미 해당 메일로 로그인한 유저가 있는 경우
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_GITHUB:
                raise GithubException(f"🧐이 계정은 [{user.login_method}]로 가입되어 있어요.")
        except models.User.DoesNotExist:
            # 해당 이메일의 유저가 존재하지 않는 경우
            user = models.User.objects.create(
                email=email,
                first_name=name,
                username=email,
                bio=bio,
                login_method=models.User.LOGIN_GITHUB,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("core:home"))
    except GithubException as error_context:
        messages.error(request, error_context)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class kakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is None:
            raise GithubException("🤔🤔카카오톡 코드를 받을 수 없어요.")
        error = request.GET.get("error", None)
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        print(token_json)
        error = token_json.get("error", None)
        if error is not None:
            raise kakaoException("😱😱카카오톡 인증 토큰을 받을 수 없어요.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        print(f"kakao_account: {kakao_account}")
        email = kakao_account.get("email", None)
        if email is None:
            raise kakaoException("😁😎가입을 위해 이메일 제공에 동의해주세요.")
        email_verified = kakao_account.get("is_email_verified")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url", None)
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise kakaoException(f"🧐이 계정은 [{user.login_method}]로 가입되어 있어요.")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=email_verified,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"{user.first_name}님, 환영합니다! 🥰")
        return redirect(reverse("core:home"))
    except kakaoException as error_context:
        messages.error(request, error_context)
        return redirect(reverse("users:login"))


class UserProfileView(mixins.LoggedInOnlyView, DetailView):
    """ UserProfileView Definition """

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    """ UpdateProfileView Definition """

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
        # "avatar",
        # to do - avatar 변경하는 form 만들기
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "🥳프로필이 변경되었습니다."

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "이름"}
        form.fields["last_name"].widget.attrs = {"placeholder": "성"}
        form.fields["gender"].widget.attrs = {"placeholder": "성별"}
        form.fields["bio"].widget.attrs = {"placeholder": "한 줄 소개"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "생년월일"}
        form.fields["language"].widget.attrs = {"placeholder": "언어"}
        form.fields["currency"].widget.attrs = {"placeholder": "통화"}
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    """ UpdatePasswordView Definition """

    template_name = "users/update_password.html"
    success_message = "😉비밀번호가 변경되었습니다."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재 비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새 비밀번호"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "새 비밀번호 확인"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


# Login
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-in

# LoginView
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
