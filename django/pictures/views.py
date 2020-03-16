from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from psycopg2.errors import UniqueViolation

from pictures.models import Picture, Favorite


# Create your views here.
def picture(request, picture_public_id):

    target_picture = Picture.objects.get(public_id=picture_public_id)

    context = {
        "photo": str(target_picture.photo),
        "title": target_picture.title,
        "tags": str(target_picture.tags).split(),
        "max_tag_length": settings.MAX_TAG_LENGTH,
        "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
    }
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
