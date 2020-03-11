from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import CustomUser

_FORM_FIELD_CLASSES = [
    "focus:outline-none",
    "focus:border-input-selected",
    "appearance-none",
    "py-3",
    "bg-surface-1",
    "opacity-high-emphasis",
    "rounded",
    "border-2",
    "border-default",
    "text-indent",
    "shadow-none",
    "border-color-transition",
    "disable-transition-on-theme-change",
]

_FORM_FIELD_ERROR_CLASSES = ["border-error"]


class CustomUserCreationForm(UserCreationForm):
    field_order = ["display_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["display_name"].widget.attrs.update(
            {"class": " ".join(_FORM_FIELD_CLASSES), "autofocus": ""}
        )

        self.fields["email"].widget.attrs.update(
            {"class": " ".join(_FORM_FIELD_CLASSES)}
        )

        self.fields["password1"].widget.attrs.update(
            {"class": " ".join(_FORM_FIELD_CLASSES)}
        )

        self.fields["password2"].widget.attrs.update(
            {"class": " ".join(_FORM_FIELD_CLASSES)}
        )

        self.fields["display_name"].initial = None

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "display_name")

    def is_valid(self):
        ret = super().is_valid()
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {
                    "class": " ".join(_FORM_FIELD_CLASSES)
                    + " "
                    + " ".join(_FORM_FIELD_ERROR_CLASSES),
                    "onfocus": "removeErrorBorder(this)",
                }
            )
        return ret


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "display_name")


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": " ".join(_FORM_FIELD_CLASSES),
                "onfocusout": "addInvalidBorder(this)",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": " ".join(_FORM_FIELD_CLASSES),
                "onfocusout": "addInvalidBorder(this)",
            }
        )

        self.error_messages["invalid_login"] = _("The email or password is incorrect.")


class UpdateDisplayNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["display_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["display_name"].widget.attrs.update(
            {"class": " ".join(_FORM_FIELD_CLASSES),}
        )
