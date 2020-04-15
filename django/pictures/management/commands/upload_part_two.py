import json
import random

from django.core.management.base import BaseCommand
from pictures.models import Picture
from users.models import CustomUser


class Command(BaseCommand):
    help = "Load pictures into the database from a json file"

    def add_arguments(self, parser):
        parser.add_argument("data_file", help="The path to the json file to load")
        parser.add_argument("--limit", help="Limit the number of images loaded")
        parser.add_argument(
            "--uploaded_by_emails",
            nargs="+",
            help=(
                "The emails to mark each image as uploaded by. "
                "If multiple are selected a random email will be "
                "chosen for each picture"
            ),
        )

    def handle(self, *args, **kwargs):
        uploaded_by_users = [
            CustomUser.objects.get(email=email)
            for email in kwargs["uploaded_by_emails"]
        ]

        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        if kwargs["limit"]:
            data = data[: kwargs["limit"]]

        for index, picture in enumerate(data):
            if index % 50 == 0:
                print(index)
            picture = Picture.objects.create(
                title=picture["title"],
                description="description",
                photo=picture["photo"],
                thumbnail_w_272=picture["thumbnail_w_272"],
                tags=" ".join(picture["tags"]),
                uploaded_by=random.choice(uploaded_by_users),
            )
            picture.save()
