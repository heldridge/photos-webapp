from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Sandbox used for testing"

    def add_arguments(self, parser):
        parser.add_argument("destination", help="The address to send the mail to")

    def handle(self, *args, **kwargs):
        send_mail(
            "Test", "This is a test!!!", "noreply@lewdix.com", [kwargs["destination"]],
        )
        print("DONE!")
