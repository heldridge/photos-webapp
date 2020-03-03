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


class Favorites(View):
    def post(self, request, picture_public_id):
        if request.user.is_authenticated:
            _, created = Favorite.objects.get_or_create(
                user=request.user,
                picture=Picture.objects.get(public_id=picture_public_id),
            )
            if created:
                return HttpResponse(status=201)
            else:
                return HttpResponse(status=200)
        else:
            pass
        return HttpResponse(status=401)

    def delete(self, request, picture_public_id):
        if request.user.is_authenticated:
            Favorite.objects.filter(
                user=request.user, picture__public_id=picture_public_id
            ).delete()
        else:
            pass
        return HttpResponse("OK")
