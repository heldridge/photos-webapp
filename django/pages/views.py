import functools
import re
import json

from django.conf import settings
from django.core import exceptions
from django.shortcuts import render


from pictures.models import Picture, Favorite, get_pictures, get_split_tags


# def get_split_tags(tags):
#     """
#     Splits an image's tags into "above" and "below" tags,
#     so they don't over-clutter the UI

#     Above and below are decided by estimating how wide
#     the resulting tag bar would be, and then putting a cap on
#     that width
#     """
#     data = {"above_tags": [], "below_tags": []}

#     max_width = 85  # Max width of the theoretical tag bar
#     expander_length = 5  # Width of the "click to expand" symbol
#     static_width_addition = 4  # How much to add in addition to each letter
#     current_width = 0
#     above = True
#     for tag in tags:
#         current_width += static_width_addition + len(tag)
#         if current_width + expander_length > max_width:
#             above = False

#         if above:
#             data["above_tags"].append(tag)
#         else:
#             data["below_tags"].append(tag)
#     return data


def clean_picture_data(picture, from_elastic_search, user=None, fetch_favorites=False):
    """
    Cleans the data from each picture, picking out the fields needed
    """
    split_tags = get_split_tags(picture.tags)

    if from_elastic_search:
        photo = picture.photo
    else:
        photo = str(picture.photo)

    return {
        "photo": photo,
        "title": picture.title,
        "above_tags": split_tags["above_tags"],
        "below_tags": split_tags["below_tags"],
        "public_id": str(picture.public_id),
        "favorite": (
            fetch_favorites
            and user is not None
            and Favorite.objects.filter(user=user).filter(picture=picture.id).exists()
        ),
    }


def is_valid_tag(tag):
    """ Verifies that a tag is valid """
    return (
        len(tag) <= settings.MAX_TAG_LENGTH
        and len(tag) >= settings.MIN_TAG_LENGTH
        and re.match(settings.VALID_TAG_REGEX, tag) is not None
    )


def stringsDoNotMatch(str1, str2):
    """ Dummy function to be used in a partial """
    return str1 != str2


def index(request):
    # Force query set evaluation because we do
    # a reverse to get the last element, after doing a slice
    pictures = list(get_pictures(settings.PAGE_SIZE + 1))

    context = {
        "pictures": [
            {"picture": picture, "tags": get_split_tags(picture.tags)}
            for picture in pictures[: settings.PAGE_SIZE]
        ],
        "grid_placeholders": [1] * (18 - len(pictures[: settings.PAGE_SIZE])),
        "more_left": len(pictures) >= settings.PAGE_SIZE + 1,
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
    }
    return render(request, "pages/index.html.j2", context)


def get_photos_data(
    tags=None, before=None, after=None, user=None, fetch_favorites=False
):
    """Given query parameters returns a photos dataset

    Args:
        tags (``list`` of ``str``): The list of tags to search for
        before (``str``): The id of the photo to fetch photos before
        after (``str``): The id of the photo to fetch photos after
        user (``user``): The user that made the request, None if not logged in
    Returns:
        {
            "photos": (``list``) The photos returned by the query
            "more_left": (``bool``) Whether there are more photos left in the current "direction"
            "first": (``photo``) The first photo in the photos list, None if the list has no items
            "last": (``photo``) The last photo in the photos list, None if the list has no items
        }
    """
    if before is not None and after is not None:
        # Can't have both
        return {"photos": [], "more_left": False, "first": None, "last": None}

    # Fetch the before or after ID
    if before is not None and before != "":
        try:
            before_picture = Picture.objects.get(public_id=before)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            before = None
    if after is not None and after != "":
        try:
            after_picture = Picture.objects.get(public_id=after)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            after = None

    # Instantiate default values
    photos = []
    more_left = True
    first = None
    last = None

    # If tags is None we can get everything from the database
    if True:  # tags is None:
        query_set = Picture.objects
        if before is not None:
            # For before we want to go "backwards," to get the pictures
            # closest in id to before_picture, so order by id (increasing)
            query_set = list(query_set.filter(id__gt=before_picture.id).order_by("id"))
        elif after is not None:
            query_set = query_set.filter(id__lt=after_picture.id).order_by("-id")
        else:
            query_set = query_set.order_by("-id")

    # If there are tags we have to go to Elasticsearch
    else:
        query_set = PictureDocument.search()

        for tag in tags:
            query_set = query_set.query("term", tags=tag)

        if before is not None:
            query_set = query_set.query("range", id={"gt": before_picture.id}).sort(
                "id"
            )
        elif after is not None:
            query_set = query_set.query("range", id={"lt": after_picture.id}).sort(
                "-id"
            )
        else:
            query_set = query_set.sort("-id")

    # Squeeze to max page size + 1 (to check if there are any left)
    query_set = list(query_set[: settings.PAGE_SIZE + 1])

    # Check if there are any left to fetch, and squeeze to the max page size
    if len(query_set) < settings.PAGE_SIZE + 1:
        more_left = False
    query_set = query_set[: settings.PAGE_SIZE]

    # We went "backwards" if we had a before, so reverse the list now
    if before is not None:
        query_set.reverse()

    photos = [
        clean_picture_data(picture, tags is not None, user, fetch_favorites)
        for picture in query_set
    ]
    if len(photos) > 0:
        first = photos[0]
        last = photos[-1]

    return {"photos": photos, "more_left": more_left, "first": first, "last": last}


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


def get_baseline_context(request, fetch_favorites=False):
    """
    Returns the base context that is shared between views
    """
    searched_tags_query_parameter = request.GET.get("q", "")
    searched_tags = list(
        set(filter(is_valid_tag, searched_tags_query_parameter.split()))
    )
    searched_tags.sort()
    searched_tags_data = []
    for tag in searched_tags:
        non_matches = functools.partial(stringsDoNotMatch, tag)
        searched_tags_data.append(
            {"tag": tag, "query": "+".join(filter(non_matches, searched_tags))}
        )

    before_picture = request.GET.get("before")
    after_picture = request.GET.get("after")

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    data = get_photos_data(
        searched_tags,
        request.GET.get("before"),
        request.GET.get("after"),
        user,
        fetch_favorites,
    )
    last_picture = data["last"]
    first_picture = data["first"]
    pictures = data["photos"]

    render_next_button, render_previous_button = get_render_next_prev(
        before_picture, after_picture, data["more_left"]
    )

    current_full_query = "+".join(searched_tags)
    if before_picture is not None:
        current_full_query += f"&before={before_picture}"
    if after_picture is not None:
        current_full_query += f"&after={after_picture}"

    return {
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
        "searched_tags_data": searched_tags_data,
        "current_query": "+".join(searched_tags),
        "current_full_query": current_full_query,
        "pictures": pictures,
        "last_picture": last_picture,
        "first_picture": first_picture,
        "render_next_button": render_next_button,
        "render_previous_button": render_previous_button,
    }


def search(request):

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

    pictures = list(
        get_pictures(settings.PAGE_SIZE + 1, before_id, after_id, searched_tags)
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

    print(render_next_button, render_previous_button)

    context = {
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
        "searched_tags_data": searched_tags_data,
        "current_query": "+".join(searched_tags),
        "pictures": [
            {"picture": picture, "tags": get_split_tags(picture.tags)}
            for picture in pictures
        ],
        "grid_placeholders": [1] * (18 - len(pictures[: settings.PAGE_SIZE])),
        "render_next_button": render_next_button,
        "render_previous_button": render_previous_button,
    }

    return render(request, "pages/search.html.j2", context)


def gallery(request):

    context = get_baseline_context(request, True)
    before_picture = request.GET.get("before")

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    # Get the gallery picture id query
    picture_id = request.GET.get("p", "")
    current_picture = None
    current_picture_index = 0
    could_not_find_picture = False
    if picture_id != "":
        try:
            current_picture = clean_picture_data(
                Picture.objects.get(public_id=picture_id), False, user, True
            )
        except (exceptions.ValidationError, Picture.DoesNotExist):
            could_not_find_picture = True
        else:
            for i, picture in enumerate(context["pictures"]):
                if picture["public_id"] == picture_id:
                    current_picture_index = i
                    break

    if (picture_id == "" or could_not_find_picture) and len(context["pictures"]) > 0:
        # We are coming in the "backwards" direction
        if before_picture is not None:
            current_picture = context["pictures"][-1]
            current_picture_index = len(context["pictures"]) - 1
        else:
            current_picture = context["pictures"][0]
            current_picture_index = 0

    original_picture_index = current_picture_index

    context["original_picture_index"] = original_picture_index
    context["pictures"] = list(
        map(
            lambda item: {
                "photo": item["photo"],
                "title": item["title"],
                "public_id": item["public_id"],
                "above_tags": item["above_tags"],
                "below_tags": item["below_tags"],
                "favorite": item["favorite"],
            },
            context["pictures"],
        )
    )
    context["grid_placeholders"] = [1] * (18 - len(context["pictures"]))
    context["picture"] = current_picture

    return render(request, "pages/gallery.html.j2", context)
