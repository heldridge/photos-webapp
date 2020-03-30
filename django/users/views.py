from django.conf import settings as project_settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View

from . import forms, models, tokens

from pictures.models import Picture, get_pictures, get_images_grid_context
from sorl.thumbnail import get_thumbnail


def profile(request):
    context = {"favorites": True}
    if request.user.is_authenticated:
        pictures = list(
            get_pictures(project_settings.PAGE_SIZE + 1, favorited_by=request.user)
        )
        context["pictures"] = get_images_grid_context(pictures)
        context["more_left"] = len(pictures) >= project_settings.PAGE_SIZE + 1
        context["grid_placeholders"] = [1] * (
            18 - len(pictures[: project_settings.PAGE_SIZE])
        )
    return render(request, "users/profile.html.j2", context=context)


def register(request):
    if request.method == "POST":
        f = forms.CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account Created Successfully!")
            return redirect("login")
    else:
        f = forms.CustomUserCreationForm()

    return render(request, "users/register.html.j2", {"form": f})


def settings(request):
    if request.method == "POST":
        f = forms.UpdateDisplayNameForm(request.POST, instance=request.user)
        if f.is_valid():
            f.save()
            messages.success(request, "Display Name Updated Successfully!")
            return redirect("settings")
    else:
        if request.user.is_authenticated:
            f = forms.UpdateDisplayNameForm(instance=request.user)
        else:
            return render(request, "users/settings.html.j2")
    return render(request, "users/settings.html.j2", {"form": f})


def user(request, user_public_id):
    context = {}
    try:
        target = models.CustomUser.objects.get(public_id=user_public_id)
    except (ObjectDoesNotExist, ValidationError):
        pass
    else:
        context["display_name"] = target.display_name
        context["search_uploaded_by"] = target.public_id

        pictures = get_pictures(project_settings.PAGE_SIZE + 1, uploaded_by=target)

        context["pictures"] = get_images_grid_context(pictures)
        context["more_left"] = len(pictures) >= project_settings.PAGE_SIZE + 1
        context["grid_placeholders"] = [1] * (
            18 - len(pictures[: project_settings.PAGE_SIZE])
        )

    return render(request, "users/user.html.j2", context)


def send_confirmation_email(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            send_mail(
                "Lewdix Email Confirmation",
                render_to_string(
                    "confirm_email.html.j2",
                    {
                        "domain": "localhost:8000",
                        "user_public_id": request.user.public_id,
                        "user_display_name": request.user.display_name,
                        "token": tokens.ACCOUNT_ACTIVATION_TOKEN.make_token(
                            request.user
                        ),
                    },
                ),
                project_settings.EMAIL_HOST_USER,
                [request.user.email],
            )
            return HttpResponse(status=200)
        return HttpResponse(status=401)
    else:
        return redirect("index")


def confirm_email(request, user_public_id, token):
    try:
        target_user = models.CustomUser.objects.get(public_id=user_public_id)
    except (ObjectDoesNotExist, ValidationError):
        target_user = None

    if target_user is not None and tokens.ACCOUNT_ACTIVATION_TOKEN.check_token(
        target_user, token
    ):
        target_user.email_confirmed = True
        target_user.save()
        messages.success(request, "Email Confirmed!")
        return redirect("index")

    return render(request, "invalid_email_confirmation.html.j2")


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "users/password_reset_email.html.j2"
    subject_template_name = "users/password_reset_subject.txt"
    template_name = "users/password_reset_request.html.j2"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["email"].widget.attrs.update(
            {"class": " ".join(project_settings.FORM_FIELD_CLASSES)}
        )
        return form


def password_reset_done(request):
    return render(request, "users/password_reset_done.html.j2")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html.j2"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update(
                {"class": " ".join(project_settings.FORM_FIELD_CLASSES)}
            )
        return form


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html.j2"


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change.html.j2"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update(
                {"class": " ".join(project_settings.FORM_FIELD_CLASSES)}
            )
        return form


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "users/password_change_done.html.j2"
