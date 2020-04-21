import datetime

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


class PictureView(View):
    def get(self, request, picture_public_id):
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

    def delete(self, request, picture_public_id):
        if request.user.is_authenticated:
            try:
                target_picture = Picture.objects.select_related("uploaded_by").get(
                    public_id=picture_public_id
                )
            except (ObjectDoesNotExist, ValidationError):
                return HttpResponse(status=404)
            else:
                if target_picture.uploaded_by == request.user:
                    target_picture.delete()
                    return HttpResponse("OK")
                else:
                    return HttpResponse(status=403)
        return HttpResponse(status=401)


def delete_success(request):
    return render(request, "picture_delete_success.html.j2")


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
        too_many_uploads = False
        if request.user.is_authenticated:
            if (
                len(request.user.last_upload_dates) >= settings.DAILY_UPLOAD_LIMIT
                and (
                    datetime.datetime.utcnow().date()
                    - request.user.last_upload_dates[-1]
                ).days
                == 0
            ):
                too_many_uploads = True
        form = PictureUploadForm()

        return render(
            request,
            "upload.html.j2",
            {
                "form": form,
                "top_tags": Tag.objects.order_by("-count")[:6],
                "too_many_uploads": too_many_uploads,
            },
        )

    def post(self, request):
        if request.user.is_authenticated and request.user.email_confirmed:
            request.user.last_upload_dates.insert(0, datetime.datetime.utcnow().date())
            request.user.save()

            if len(request.user.last_upload_dates) > settings.DAILY_UPLOAD_LIMIT:
                # The user has made too many previous uploads

                # We need to pop off the oldest request
                oldest_upload = request.user.last_upload_dates.pop()
                request.user.save()

                if (datetime.datetime.utcnow().date() - oldest_upload).days == 0:
                    # The oldest upload is less than 24 hours old
                    messages.error(
                        request,
                        (
                            "You have reached the daily upload limit. Please wait 24 "
                            "hours before attempting further uploads."
                        ),
                    )
                    return redirect("upload")

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


def tags(request):
    # order = request.GET.get("order", "most_used")
    # page = request.GET.get("page", 0)
    letter = request.GET.get("letter", "")

    loaded_tags = Tag.objects.all().order_by("-count")

    if letter:
        loaded_tags = loaded_tags.filter(title__startswith=letter)
    return render(
        request,
        "tags.html.j2",
        context={"tags": loaded_tags[: settings.TAGS_PAGE_SIZE], "letter": letter},
    )
