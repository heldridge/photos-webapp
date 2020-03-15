import datetime
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture


class Command(BaseCommand):
    help = "Load pictures into the database from a json file"

    def add_arguments(self, parser):
        parser.add_argument("data_file", help="The path to the json file to load")

    def handle(self, *args, **kwargs):
        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        for image in data:
            picture = Picture.objects.create(
                title=image["title"],
                description="description",
                photo=f'pictures/2020/01/01/{image["filename"]}',
                uploaded_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                tags=" ".join(image["tags"]),
            )
            picture.save()
