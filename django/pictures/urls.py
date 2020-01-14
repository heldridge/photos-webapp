from django.urls import path
from . import views

urlpatterns = [
    path("<str:picture_public_id>", views.picture, name="picture"),
]
