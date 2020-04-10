from django.urls import path
from . import views

urlpatterns = [
    path("<str:picture_public_id>", views.PictureView.as_view(), name="picture"),
    path("<str:picture_public_id>/favorites/", views.Favorites.as_view()),
    path("upload/", views.Upload.as_view(), name="upload"),
]
