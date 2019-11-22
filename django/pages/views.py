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
    new_pictures = []
    for picture in pictures:
        new_pictures.append(clean_picture_data(picture, from_elastic_search))
    return new_pictures


def getLatestPictures(from_elastic_search=True, tags=[]):
    if from_elastic_search:
        pictures = PictureDocument.search()
        for tag in tags:
            pictures = pictures.query("term", tags=tag)
        pictures = pictures.sort("-id")[:16]
    else:
        pictures = Picture.objects.order_by("-uploaded_at")[:16]
    return clean_pictures(pictures, from_elastic_search)


def is_valid_tag(tag):
    return (
        len(tag) <= settings.MAX_TAG_LENGTH
        and len(tag) >= settings.MIN_TAG_LENGTH
        and re.match(settings.VALID_TAG_REGEX, tag) is not None
    )


def index(request):
    context = {"pictures": getLatestPictures(False), "grid_placeholders": [1, 2]}
    return render(request, "pages/index.html.j2", context)


def stringsDoNotMatch(str1, str2):
    return str1 != str2


def search(request):
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

    pictures = getLatestPictures(
        tags=[tag_data["tag"] for tag_data in searched_tags_data]
    )
    if len(pictures) > 0:
        last_picture = pictures[-1]
    else:
        last_picture = None

    context = {
        "pictures": pictures,
        "grid_placeholders": [1, 2],
        "searched_tags_data": searched_tags_data,
        "current_query": "+".join(searched_tags),
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
        "last_picture": last_picture,
    }
    return render(request, "pages/search.html.j2", context)


def gallery(request):
    context = {}
    return render(request, "pages/gallery.html.j2", context)
