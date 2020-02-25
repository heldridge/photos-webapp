from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def profile(request):
    return render(request, "users/profile.html.j2")


def register(request):

    if request.method == "POST":
        f = forms.CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect("login")
    else:
        f = forms.CustomUserCreationForm()

    return render(request, "users/register.html.j2", {"form": f})
