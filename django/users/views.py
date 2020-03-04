from django.contrib import messages
from django.shortcuts import render, redirect
from . import forms

from pictures.models import Picture, Favorite


def get_split_tags(tags):
    """
    Splits an image's tags into "above" and "below" tags,
    so they don't over-clutter the UI

    Above and below are decided by estimating how wide
    the resulting tag bar would be, and then putting a cap on
    that width
    """
    data = {"above_tags": [], "below_tags": []}

    max_width = 85  # Max width of the theoretical tag bar
    expander_length = 5  # Width of the "click to expand" symbol
    static_width_addition = 4  # How much to add in addition to each letter
    current_width = 0
    above = True
    for tag in tags:
        current_width += static_width_addition + len(tag)
        if current_width + expander_length > max_width:
            above = False

        if above:
            data["above_tags"].append(tag)
        else:
            data["below_tags"].append(tag)
    return data


def clean_picture_data(picture):
    """
    Cleans the data from each picture, picking out the fields needed
    """
    split_tags = get_split_tags(picture.tags)
    photo = str(picture.photo)

    return {
        "photo": photo,
        "title": picture.title,
        "above_tags": split_tags["above_tags"],
        "below_tags": split_tags["below_tags"],
        "public_id": str(picture.public_id),
    }


# Create your views here.
def profile(request):
    context = {}
    if request.user.is_authenticated:
        # favorites = Favorite.objects.filter(user=request.user).order_by("id")
        favorites = Picture.objects.filter(favorite__user=request.user).order_by("id")
        context["pictures"] = [clean_picture_data(picture) for picture in favorites]

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
