from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "아이디와 비밀번호를 확인해주세요."
        ),
        "inactive": _("This account is inactive."),
    }


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("새로운 비밀번호가 일치하지 않습니다."),
    }

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].label = '아이디'
        self.fields['nickname'].label = '닉네임'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("새로운 비밀번호가 일치하지 않습니다."),
        "password_incorrect": _(
            "기존 비밀번호가 일치하지 않습니다."
        ),
    }
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['new_password1'].label = '새로운 비밀번호'
        self.fields['new_password2'].label = '새로운 비밀번호 확인'
        self.fields['new_password1'].help_text = ''

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

class CustomMinimumLengthValidator(DjangoMinimumLengthValidator):
    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters. Please make it longer."
        ) % {"min_length": self.min_length}