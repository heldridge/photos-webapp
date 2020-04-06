import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    display_name = models.CharField(max_length=30, default="Unknown")
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email_confirmed = models.BooleanField(default=False)
    last_email_dates = ArrayField(models.DateField(blank=True), size=5, default=list)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
