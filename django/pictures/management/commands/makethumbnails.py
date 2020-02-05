from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture

from sorl.thumbnail import get_thumbnail


class Command(BaseCommand):
    help = "Generate thumbnails for images in the database"

    def handle(self, *args, **kwargs):
        print("Generating thumbnails...")
        counter = 0
        for picture in Picture.objects.all():
            for size in settings.THUMBNAIL_SIZES:
                get_thumbnail(picture.photo, size)
            counter += 1
            if counter % 50 == 0:
                print(counter)
