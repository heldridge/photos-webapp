import functools
import re

from django.conf import settings
from django.shortcuts import render

from pictures.models import Picture
from pictures.documents import PictureDocument


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


def clean_picture_data(picture, from_elastic_search):
    """
    Cleans the data from each picture, picking out the fields needed
    """
    split_tags = get_split_tags(picture.tags)

    if from_elastic_search:
        photo = picture.photo
    else:
        photo = picture.photo.url

    return {
        "photo": photo,
        "title": picture.title,
        "above_tags": split_tags["above_tags"],
        "below_tags": split_tags["below_tags"],
        "public_id": str(picture.public_id),
    }


def clean_pictures(pictures, from_elastic_search):
    """ Cleans each picture in a dataset """
    new_pictures = []
    for picture in pictures:
        new_pictures.append(clean_picture_data(picture, from_elastic_search))
    return new_pictures


def search_pictures(tags=[], after_picture=None, before_picture=None):
    """ Queries elastic search """
    pictures = PictureDocument.search()
    if after_picture is not None:
        pictures = pictures.query("range", id={"lt": after_picture.id})
    if before_picture is not None:
        pictures = pictures.query("range", id={"gt": before_picture.id})

    for tag in tags:
        pictures = pictures.query("term", tags=tag)

    if before_picture is None:
        pictures = pictures.sort("-id")[: settings.PAGE_SIZE + 1]
    else:
        pictures = list(pictures.sort("id")[: settings.PAGE_SIZE + 1])
        pictures.reverse()

    return [clean_picture_data(picture, True) for picture in pictures]


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
    # pictures = clean_pictures(
    #     Picture.objects.order_by("-uploaded_at")[: settings.PAGE_SIZE + 1], False
    # )
    pictures = get_photos_data()["photos"]

    render_continue_button = len(pictures) >= settings.PAGE_SIZE + 1

    pictures = pictures[: settings.PAGE_SIZE]
    last_picture = None
    if len(pictures) > 0:
        last_picture = pictures[-1]

    context = {
        "pictures": pictures,
        "grid_placeholders": [1] * (18 - len(pictures)),
        "last_picture": last_picture,
        "render_continue_button": render_continue_button,
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
    }
    return render(request, "pages/index.html.j2", context)


def get_photos_data(tags=[], before=None, after=None):
    """Given query parameters returns a photos dataset

    Args:
        tags (``list`` of ``str``): The list of tags to search for
        before (``str``): The id of the photo to fetch photos before
        after (``str``): The id of the photo to fetch photos after
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
        before_picture = Picture.objects.get(public_id=before)
    if after is not None and after != "":
        after_picture = Picture.objects.get(public_id=after)

    photos = []
    more_left = True
    first = None
    last = None

    if tags == []:
        query_set = Picture.objects
        if before is not None:
            query_set = list(
                query_set.filter(id__gt=before_picture.id).order_by("id")[
                    : settings.PAGE_SIZE + 1
                ]
            )
        elif after is not None:
            query_set = query_set.filter(id__lt=after_picture.id).order_by("-id")[
                : settings.PAGE_SIZE + 1
            ]
            if len(query_set) < settings.PAGE_SIZE + 1:
                more_left = False
        else:
            query_set = query_set.order_by("-id")[: settings.PAGE_SIZE + 1]

        if len(query_set) < settings.PAGE_SIZE + 1:
            more_left = False
        query_set = query_set[: settings.PAGE_SIZE]

        if before is not None:
            query_set.reverse()

        query_set = list(query_set)
        photos = [clean_picture_data(picture, False) for picture in query_set]
        if len(photos) > 0:
            first = photos[0]
            last = photos[-1]

    else:
        x = ""
        # fetch from elasticsearch

    return {"photos": photos, "more_left": more_left, "first": first, "last": last}


def search(request):
    # Grab and validate tags
    # Also remove duplicates
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

    # after = request.GET.get("after", "")
    # after_picture = None
    # if after != "":
    #     # Grab the internal id from postgres
    #     after_picture = Picture.objects.get(public_id=after)

    # before = request.GET.get("before", "")
    # before_picture = None
    # if before != "":
    #     # Grab the internal id from postgres
    #     before_picture = Picture.objects.get(public_id=before)

    # pictures = search_pictures(
    #     tags=[tag_data["tag"] for tag_data in searched_tags_data],
    #     after_picture=after_picture,
    #     before_picture=before_picture,
    # )

    # render_next_button = True
    # render_previous_button = True

    # # Raw fetch, no before / after
    # if before_picture is None and after_picture is None:
    #     render_previous_button = False
    #     if len(pictures) < settings.PAGE_SIZE + 1:
    #         render_next_button = False

    # # We have done a before / after, so disabling is done on the
    # # direction we're going
    # if len(pictures) < settings.PAGE_SIZE + 1:
    #     if before_picture is not None:
    #         render_previous_button = False
    #     elif after_picture is not None:
    #         render_next_button = False

    # # If we were going backwards we want to shave off the first
    # # pic, not the last, so reverse before and after the shave
    # if before_picture is not None:
    #     pictures.reverse()
    # pictures = pictures[: settings.PAGE_SIZE]
    # if before_picture is not None:
    #     pictures.reverse()

    # if len(pictures) > 0:
    #     last_picture = pictures[-1]
    #     first_picture = pictures[0]
    # else:
    #     last_picture = None
    #     first_picture = None

    before_picture = request.GET.get("before")
    after_picture = request.GET.get("after")

    data = get_photos_data([], request.GET.get("before"), request.GET.get("after"))
    last_picture = data["last"]
    first_picture = data["first"]
    pictures = data["photos"]

    render_next_button = True
    render_previous_button = True

    if before_picture is None and after_picture is None:
        render_previous_button = False
        if not data["more_left"]:
            render_next_button = False

    if before_picture is not None and not data["more_left"]:
        render_previous_button = False

    if after_picture is not None and not data["more_left"]:
        render_next_button = False

    context = {
        "pictures": pictures,
        "grid_placeholders": [1] * (18 - len(pictures)),
        "searched_tags_data": searched_tags_data,
        "current_query": "+".join(searched_tags),
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
        "last_picture": last_picture,
        "first_picture": first_picture,
        "render_next_button": render_next_button,
        "render_previous_button": render_previous_button,
    }
    return render(request, "pages/search.html.j2", context)


def gallery(request):
    context = {}
    return render(request, "pages/gallery.html.j2", context)
