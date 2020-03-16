from django.core.management.base import BaseCommand
from pictures.models import Picture


class Command(BaseCommand):
    help = "Deletes all photos from the database"

    def handle(self, *args, **kwargs):
        Picture.objects.all().delete()
