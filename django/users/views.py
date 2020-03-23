from django.conf import settings as project_settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from . import forms, models

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

