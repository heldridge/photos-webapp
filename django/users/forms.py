from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["display_name"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                # "onfocusout": "addInvalidBorder(this)",
            }
        )

        self.fields["email"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                # "onfocusout": "addInvalidBorder(this)",
            }
        )

        self.fields["password1"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                # "onfocusout": "addInvalidBorder(this)",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                # "onfocusout": "addInvalidBorder(this)",
            }
        )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "display_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "display_name")


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                "onfocusout": "addInvalidBorder(this)",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "focus:outline-none focus:border-input-selected appearance-none py-3 bg-surface-1 opacity-high-emphasis rounded border-2 border-default text-indent shadow-none border-color-transition disable-transition-on-theme-change",
                "onfocusout": "addInvalidBorder(this)",
            }
        )

        self.error_messages["invalid_login"] = _("The email or password is incorrect.")
