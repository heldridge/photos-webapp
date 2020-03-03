from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from psycopg2.errors import UniqueViolation

from pictures.models import Picture, Favorite


def clean_picture_data(picture, from_elastic_search):
    """
    TODO: Consolidate with other
    Cleans the data from each picture, picking out the fields needed
    """
    if from_elastic_search:
        photo = picture.photo
    else:
        photo = picture.photo.url

    print(picture.tags)

    return {
        "photo": photo,
        "title": picture.title,
        "tags": picture.tags,
        "public_id": str(picture.public_id),
    }


# Create your views here.
def picture(request, picture_public_id):
    my_picture = Picture.objects.get(public_id=picture_public_id)

    context = clean_picture_data(my_picture, False)
    context["max_tag_length"] = settings.MAX_TAG_LENGTH
    context["invalid_tag_char_regex"] = settings.INVALID_TAG_CHAR_REGEX

    return render(request, "picture.html.j2", context)


class AddFavorite(View):
    def post(self, request, picture_public_id):
        if request.user.is_authenticated:
            fav, created = Favorite.objects.get_or_create(
                user=request.user,
                picture=Picture.objects.get(public_id=picture_public_id),
            )
        else:
            pass
        return HttpResponse("OK")
