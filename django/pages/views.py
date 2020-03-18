import functools
import re
import json

from django.conf import settings
from django.core import exceptions
from django.db.models import Q
from django.shortcuts import render


from pictures.models import Picture, Favorite, get_pictures


def is_valid_tag(tag):
    """ Verifies that a tag is valid """
    return (
        len(tag) <= settings.MAX_TAG_LENGTH
        and len(tag) >= settings.MIN_TAG_LENGTH
        and re.match(settings.VALID_TAG_REGEX, tag) is not None
    )


def get_render_next_prev(before_picture, after_picture, more_left):
    render_next_button = True
    render_previous_button = True

    if before_picture is None and after_picture is None:
        render_previous_button = False
        if not more_left:
            render_next_button = False

    if before_picture is not None and not more_left:
        render_previous_button = False

    if after_picture is not None and not more_left:
        render_next_button = False

    return (render_next_button, render_previous_button)


def index(request):
    # Force query set evaluation because we do
    # a reverse to get the last element, after doing a slice
    pictures = list(get_pictures(settings.PAGE_SIZE + 1))

    context = {
        "pictures": pictures[: settings.PAGE_SIZE],
        "grid_placeholders": [1] * (18 - len(pictures[: settings.PAGE_SIZE])),
        "more_left": len(pictures) >= settings.PAGE_SIZE + 1,
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
    }
    return render(request, "pages/index.html.j2", context)


def get_shared_search_gallery_context(request):
    # Filter out invalid tags
    # Use SET to make all unique
    # cast as a list because easier to use
    searched_tags = list(set(filter(is_valid_tag, request.GET.get("q", "").split())))

    searched_tags_data = []
    for tag in searched_tags:
        searched_tags_data.append(
            {
                "tag": tag,
                "query_if_removed": "+".join(
                    filter(lambda newTag: newTag != tag, searched_tags)
                ),
            }
        )

    before_id = request.GET.get("before")
    after_id = request.GET.get("after")

    search_favorites = request.GET.get("favorites", "false")

    if search_favorites == "true" and request.user.is_authenticated:
        user = request.user
    else:
        user = None

    pictures = list(
        get_pictures(settings.PAGE_SIZE + 1, before_id, after_id, searched_tags, user)
    )

    # Truncate before the reverse so the correct image gets truncated
    more_left = len(pictures) >= settings.PAGE_SIZE + 1
    pictures = pictures[: settings.PAGE_SIZE]
    # Search goes backwards if before is specified
    if before_id is not None:
        pictures.reverse()

    render_next_button, render_previous_button = get_render_next_prev(
        before_id, after_id, more_left
    )

    return {
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
        "searched_tags_data": searched_tags_data,
        # "current_query": "+".join(searched_tags),
        "pictures": pictures,
        "grid_placeholders": [1] * (18 - len(pictures[: settings.PAGE_SIZE])),
        "render_next_button": render_next_button,
        "render_previous_button": render_previous_button,
        "q": "+".join(searched_tags),
        "before_id": before_id,
        "after_id": after_id,
        "favorites": search_favorites == "true",
    }


def search(request):
    context = get_shared_search_gallery_context(request)
    return render(request, "pages/search.html.j2", context)


def gallery(request):
    context = get_shared_search_gallery_context(request)

    picture_id = request.GET.get("p", "")
    current_picture = None
    current_picture_index = 0
    could_not_find_picture = False
    if picture_id != "":
        try:
            current_picture = Picture.objects.get(public_id=picture_id)

        except (exceptions.ValidationError, Picture.DoesNotExist):
            could_not_find_picture = True
        else:
            for i, picture in enumerate(context["pictures"]):
                if str(picture.public_id) == picture_id:
                    current_picture_index = i
                    break

    if (picture_id == "" or could_not_find_picture) and len(context["pictures"]) > 0:
        if request.GET.get("before") is None or request.GET.get("before") == "":
            current_picture = context["pictures"][0]
            current_picture_index = 0
        else:
            current_picture = context["pictures"][-1]
            current_picture_index = len(context["pictures"]) - 1

    original_picture_index = current_picture_index
    context["original_picture_index"] = original_picture_index

    favorite_ids = []
    if request.user.is_authenticated and len(context["pictures"]) > 0:
        favorites = Favorite.objects.select_related("picture").filter(user=request.user)
        full_q = Q(picture=context["pictures"][0])
        for picture in context["pictures"][1:]:
            full_q = full_q | Q(picture=picture)
        favorites = favorites.filter(full_q)

        for favorite in favorites:
            favorite_ids.append(favorite.picture.public_id)

    # Need to make it json serializable
    context["pictures"] = list(
        map(
            lambda picture: {
                "photo": str(picture.photo),
                "title": picture.title,
                "public_id": picture.public_id,
                "tags": str(picture.tags).split(),
                "favorite": picture.public_id in favorite_ids,
            },
            context["pictures"],
        )
    )
    context["picture"] = current_picture

    return render(request, "pages/gallery.html.j2", context)
