from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Sandbox used for testing"

    def handle(self, *args, **kwargs):
        send_mail(
            "Dinner?",
            "Hi Harry, was just wondering if you wanted to do dinner tonight",
            settings.EMAIL_HOST_USER,
            ["zirapa@gmail.com"],
        )
        print("DONE!")
