from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
    path("profile/settings", views.settings, name="settings"),
    path("users/<str:user_public_id>", views.user, name="users"),
    path(
        "send-confirmation-email",
        views.send_confirmation_email,
        name="send_confirmation_email",
    ),
    path(
        "confirm-email/<str:user_public_id>/<str:token>",
        views.confirm_email,
        name="confirm_email",
    ),
]
