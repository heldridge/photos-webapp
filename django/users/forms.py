from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
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

