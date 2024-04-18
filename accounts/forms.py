from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator, exceeds_maximum_length_ratio, SequenceMatcher
from django import forms
from django.core.exceptions import ValidationError, FieldDoesNotExist
import re


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "아이디와 비밀번호를 확인해주세요."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password'].help_text = ''
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control mb-2 custom-form-input'
        self.fields['password'].widget.attrs['class'] = 'form-control mb-2 custom-form-input'
        self.fields['username'].widget.attrs['placeholder'] = '아이디'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호'


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
        self.fields['username'].label = ''
        self.fields['nickname'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control mb-2 custom-form-input'
        self.fields['nickname'].widget.attrs['class'] = 'form-control mb-2 custom-form-input'
        self.fields['password1'].widget.attrs['class'] = 'form-control mb-2 custom-form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-control mb-3 custom-form-input'
        self.fields['username'].widget.attrs['placeholder'] = '아이디'
        self.fields['nickname'].widget.attrs['placeholder'] = '닉네임'
        self.fields['password1'].widget.attrs['placeholder'] = '비밀번호'
        self.fields['password2'].widget.attrs['placeholder'] = '비밀번호 확인'
        
    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": "이미 존재하는 아이디 입니다."
                        
                    }
                )
            )
        else:
            return username

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

class CustomMinimunMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "비밀번호가 너무 짧습니다. 비밀번호는 적어도 "
                    "%(min_length)d자 이상이어야 합니다.",
                    "비밀번호가 너무 짧습니다. 비밀번호는 적어도 "
                    "%(min_length)d자 이상이어야 합니다.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator) :
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("비밀번호가 %(verbose_name)s와 유사합니다."),
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("비밀번호에 중복이 너무 많습니다.."),
                code="password_too_common",
            )
        
class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("비밀번호는 숫자로 이루어질 수 없습니다."),
                code="password_entirely_numeric",
            )

