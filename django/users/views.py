from django.conf import settings as project_settings
from django.contrib import messages
from django.shortcuts import render, redirect
from . import forms

from pictures.models import Picture, Favorite


def profile(request):
    context = {}
    if request.user.is_authenticated:
        pictures = Picture.objects.filter(favorite__user=request.user).order_by("-id")[
            : project_settings.PAGE_SIZE + 1
        ]
        context["pictures"] = pictures[: project_settings.PAGE_SIZE]
        context["more_left"] = len(pictures) >= project_settings.PAGE_SIZE + 1

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
