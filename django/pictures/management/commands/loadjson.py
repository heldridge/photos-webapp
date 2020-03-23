import datetime
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pictures.models import Picture
from users.models import CustomUser


class Command(BaseCommand):
    help = "Load pictures into the database from a json file"

    def add_arguments(self, parser):
        parser.add_argument("data_file", help="The path to the json file to load")
        parser.add_argument("--limit", help="Limit the number of images loaded")
        parser.add_argument(
            "--uploaded_by_email",
            help="The email of the user to mark each image as uploaded by",
            default="harry@example.com",
        )

    def handle(self, *args, **kwargs):
        uploaded_by_user = CustomUser.objects.get(email=kwargs["uploaded_by_email"])

        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        if kwargs["limit"]:
            data = data[: kwargs["limit"]]

        for index, image in enumerate(data):
            if index % 50 == 0:
                print(index)
            picture = Picture.objects.create(
                title=image["title"],
                description="description",
                photo=f'pictures/2020/01/01/{image["filename"]}',
                tags=" ".join(image["tags"]),
                uploaded_by=uploaded_by_user,
            )
            picture.save()
