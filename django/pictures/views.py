from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from psycopg2.errors import UniqueViolation
from django.contrib import messages
from django.shortcuts import render, redirect

from pictures.models import Picture, Favorite, Tag
from .forms import PictureUploadForm


# Create your views here.
def picture(request, picture_public_id):
    render_delete_button = False
    try:
        target_picture = Picture.objects.select_related("uploaded_by").get(
            public_id=picture_public_id
        )
    except (ObjectDoesNotExist, ValidationError):
        # ObjectDoesNotExist for a uuid not in pictures
        # ValidationError for a bad uuid
        context = {}
    else:
        favorite = False
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user=request.user).filter(
                picture=target_picture
            )
            if favorites.count() > 0:
                favorite = True

            if target_picture.uploaded_by == request.user:
                render_delete_button = True

        context = {
            "public_id": str(target_picture.public_id),
            "photo": target_picture.photo,
            "title": target_picture.title,
            "tags": str(target_picture.tags).split(),
            "favorite": favorite,
            "max_tag_length": settings.MAX_TAG_LENGTH,
            "invalid_tag_char_regex": settings.INVALID_TAG_CHAR_REGEX,
            "uploaded_by_public_id": str(target_picture.uploaded_by.public_id)
            if target_picture.uploaded_by is not None
            else None,
            "uploaded_by_display_name": str(target_picture.uploaded_by.display_name)
            if target_picture.uploaded_by is not None
            else None,
            "render_delete_button": render_delete_button,
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

        return HttpResponse("OK")


class Upload(View):
    def get(self, request):
        form = PictureUploadForm()

        return render(
            request,
            "upload.html.j2",
            {"form": form, "top_tags": Tag.objects.order_by("-count")[:6]},
        )

    def post(self, request):
        if request.user.is_authenticated and request.user.email_confirmed:
            form = PictureUploadForm(request.POST, request.FILES)
            if form.is_valid():
                new_picture = form.save(commit=False)
                new_picture.uploaded_by = request.user
                new_picture.save()

                messages.success(request, "Upload Complete!")
                return redirect("upload")
            else:
                return render(
                    request,
                    "upload.html.j2",
                    {"form": form, "top_tags": Tag.objects.order_by("-count")[:6]},
                )
        else:
            form = PictureUploadForm()
            messages.error(
                request,
                "You must be logged in with a confirmed email to upload content",
            )
            return render(
                request,
                "upload.html.j2",
                {"form": form, "top_tags": Tag.objects.order_by("-count")[:6]},
            )
