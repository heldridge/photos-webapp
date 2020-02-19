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

        self.fields["username"].widget.attrs.update({"class": "lmaoooo"})

