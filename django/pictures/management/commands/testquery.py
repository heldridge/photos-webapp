from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture


class Command(BaseCommand):
    help = "Generate thumbnails for images in the database"

    def handle(self, *args, **kwargs):
        print(Picture.objects.filter(tags__title="beach"))
