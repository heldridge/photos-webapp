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
    path(
        "reset", views.CustomPasswordResetView.as_view(), name="password_reset_request",
    ),
    path("reset/done", views.password_reset_done, name="password_reset_done",),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password-change",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change-done",
        views.CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
