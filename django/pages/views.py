import functools
import re
import json

from django.conf import settings
from django.core import exceptions
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.utils.html import escape


from pictures.models import (
    Picture,
    Favorite,
    get_pictures,
    get_images_grid_context,
    Tag,
)
from users.models import CustomUser
from sorl.thumbnail import get_thumbnail


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
    pictures = list(
        get_pictures(settings.PAGE_SIZE + 1).annotate(models.Count("favorite"))
    )

    # Note: Bad performance is due to calling thumbnailer in template

    # thumbs = [str(get_thumbnail(picture.photo, '272')) for picture in pictures]
    # print(thumbs)

    print([pic.favorite__count for pic in pictures])

    context = {
        "pictures": get_images_grid_context(pictures),
        "grid_placeholders": [1] * (18 - len(pictures[: settings.PAGE_SIZE])),
        "more_left": len(pictures) >= settings.PAGE_SIZE + 1,
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
        "top_tags": Tag.objects.order_by("-count")[:10],
    }
    return render(request, "pages/index.html.j2", context)


def get_shared_search_gallery_context(
    request, get_uploaded_by=False, get_num_favs=False
):
    # Filter out invalid tags
    # Use SET to make all unique
    # cast as a list because easier to use
    searched_tags = list(set(filter(is_valid_tag, request.GET.get("tags", "").split())))

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

    search_order = request.GET.get("order")

    before_id = request.GET.get("before")
    after_id = request.GET.get("after")

    search_favorites = request.GET.get("favorites", "false")

    if search_favorites == "true" and request.user.is_authenticated:
        user = request.user
    else:
        user = None

    fetch_pictures = True
    search_uploaded_by = request.GET.get("uploaded_by")
    if search_uploaded_by:
        try:
            search_uploaded_by = CustomUser.objects.get(public_id=search_uploaded_by)
        except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
            search_uploaded_by = None
            fetch_pictures = False
            pictures = Picture.objects.none()

    if fetch_pictures:
        pictures = list(
            get_pictures(
                settings.PAGE_SIZE + 1,
                before_id,
                after_id,
                searched_tags,
                favorited_by=user,
                uploaded_by=search_uploaded_by,
                get_uploaded_by=get_uploaded_by,
                order=search_order,
                get_num_favs=get_num_favs,
            )
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
        "tags": "+".join(searched_tags),
        "before_id": before_id,
        "after_id": after_id,
        "favorites": search_favorites == "true",
        "search_uploaded_by": str(search_uploaded_by.public_id)
        if search_uploaded_by
        else None,
        "search_uploaded_by_display_name": str(search_uploaded_by.display_name)
        if search_uploaded_by
        else None,
        "main_qsp": {
            "tags": "+".join(searched_tags),
            "favorites": "true" if search_favorites == "true" else False,
            "uploaded_by": str(search_uploaded_by.public_id)
            if search_uploaded_by
            else None,
            "order": search_order,
        },
    }


def search(request):
    context = get_shared_search_gallery_context(request, get_num_favs=True)

    context["pictures"] = get_images_grid_context(context["pictures"])

    return render(request, "pages/search.html.j2", context)


def gallery(request):
    context = get_shared_search_gallery_context(request, get_uploaded_by=True)

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
                "title": escape(picture.title),
                "public_id": picture.public_id,
                "tags": escape(str(picture.tags)).split(),
                "favorite": picture.public_id in favorite_ids,
                "thumbnail": picture.thumbnail_w_272.url,
                "uploaded_by_public_id": str(picture.uploaded_by.public_id)
                if picture.uploaded_by is not None
                else None,
                "uploaded_by_display_name": escape(
                    str(picture.uploaded_by.display_name)
                )
                if picture.uploaded_by is not None
                else None,
            },
            context["pictures"],
        )
    )
    context["picture"] = current_picture

    context["change_page_base_query"] = "&".join(
        [
            f"{name}={value}"
            for name, value in filter(lambda item: item[1], context["main_qsp"].items())
        ]
    )

    if settings.USE_S3:
        context["media_prefix"] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}"
    else:
        context["media_prefix"] = ""

    return render(request, "pages/gallery.html.j2", context)


def feedback(request):
    return render(request, "pages/feedback.html.j2")
