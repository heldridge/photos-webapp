from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from users.models import CustomUser


class Command(BaseCommand):
    help = "Remove a email_confirmed status from a user"

    def add_arguments(self, parser):
        parser.add_argument("email", help="The email of the user to dereg")

    def handle(self, *args, **kwargs):
        user = CustomUser.objects.get(email=kwargs["email"])
        user.email_confirmed = False
        user.save()
        print("Done!")
