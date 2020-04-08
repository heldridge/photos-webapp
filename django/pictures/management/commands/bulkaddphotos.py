import datetime
import json
import os
import pathlib
import uuid

import boto3

from django.conf import settings
from django.core.management.base import BaseCommand
from pictures.models import Picture
from users.models import CustomUser


class Command(BaseCommand):
    help = "Load pictures into the database from a json file"

    def add_arguments(self, parser):
        parser.add_argument("data_file", help="The path to the json file to load")
        parser.add_argument("images_dir", help="path to the directory with the images")
        parser.add_argument("--limit", help="Limit the number of images loaded")
        parser.add_argument(
            "--uploaded_by_email",
            help="The email of the user to mark each image as uploaded by",
        )

    def handle(self, *args, **kwargs):
        uploaded_by_user = CustomUser.objects.get(email=kwargs["uploaded_by_email"])

        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        if kwargs["limit"]:
            data = data[: int(kwargs["limit"])]

        s3 = boto3.resource("s3")
        bucket = s3.Bucket("media.qlbhmmvpym.club")

        for index, image in enumerate(data):
            public_id = str(uuid.uuid4())

            extension = os.path.splitext(image["filename"])[1]

            path_start = "pictures/" + datetime.datetime.utcnow().strftime("%Y/%m/%d/")

            bucket.upload_file(
                str(pathlib.Path(kwargs["images_dir"], image["filename"])),
                "media/" + path_start + public_id + extension,
            )

            picture = Picture.objects.create(
                public_id=public_id,
                title=image["title"],
                description="description",
                photo=path_start + public_id + extension,
                tags=" ".join(image["tags"]),
                uploaded_by=uploaded_by_user,
            )
            picture.save()

            if index % 50 == 0:
                print(index)
