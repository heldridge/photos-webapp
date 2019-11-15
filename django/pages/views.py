import functools
import re

from django.conf import settings
from django.shortcuts import render

from pictures.models import Picture
from pictures.documents import PictureDocument


def split_tags(pictures):
    max_width = 85
    expander_length = 5
    static_width_addition = 4
    updated_pictures = []
    for picture in pictures:
        data = {"above_tags": [], "below_tags": []}
        current_width = 0
        above = True
        for tag in picture.tags:
            current_width += static_width_addition + len(tag)
            if current_width + expander_length > max_width:
                above = False

            if above:
                data["above_tags"].append(tag)
            else:
                data["below_tags"].append(tag)

        updated_pictures.append(data)
    return updated_pictures


def getLatestPictures():
    # pictures = Picture.objects.order_by("-uploaded_at")[:16]
    pictures = PictureDocument.search().sort("-id")[:16]
    print([p.photo for p in pictures])
    return split_tags(pictures)


def is_valid_tag(tag):
    return (
        len(tag) <= settings.MAX_TAG_LENGTH
        and len(tag) >= settings.MIN_TAG_LENGTH
        and re.match(settings.VALID_TAG_REGEX, tag) is not None
    )


def index(request):
    context = {"pictures": getLatestPictures(), "grid_placeholders": [1, 2]}
    return render(request, "pages/index.html.j2", context)


def stringsDoNotMatch(str1, str2):
    return str1 != str2


def search(request):

    # s = PictureDocument.search().query("term", tags="person").sort("-id")[:15]
    s = PictureDocument.search().sort("-id")[:15]

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

    context = {
        "pictures": getLatestPictures(),
        "grid_placeholders": [1, 2],
        "searched_tags_data": searched_tags_data,
        "current_query": "+".join(searched_tags),
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "min_tag_length": settings.MIN_TAG_LENGTH,
        "valid_tag_regex": settings.VALID_TAG_REGEX,
    }
    return render(request, "pages/search.html.j2", context)
