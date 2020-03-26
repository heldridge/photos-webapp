from django.conf import settings as project_settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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
    return HttpResponse(200)
