from django.urls import path
from . import views

urlpatterns = [
    path("tags", views.tags, name="tags"),
    path("tags/", views.tags, name="regular_tags"),
    path("delete-success", views.delete_success, name="delete_success"),
    path("<str:picture_public_id>", views.PictureView.as_view(), name="picture"),
    path("<str:picture_public_id>/favorites/", views.Favorites.as_view()),
    path("upload/", views.Upload.as_view(), name="upload"),
]
