import datetime
import json
import os
import pathlib
import random
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
        parser.add_argument(
            "--images_dir", help="path to the directory with the images"
        )
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
        parser.add_argument(
            "--upload_photos",
            action="store_true",
            help=(
                "Whether to upload the photos to s3. Requires "
                "--images-dir to be specified"
            ),
        )

    def handle(self, *args, **kwargs):
        users = [
            CustomUser.objects.get(email=email)
            for email in kwargs["uploaded_by_emails"]
        ]

        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        if kwargs["limit"]:
            data = data[: int(kwargs["limit"])]

        if kwargs["upload_photos"]:
            s3 = boto3.resource("s3")
            bucket = s3.Bucket("media.qlbhmmvpym.club")

        for index, image in enumerate(data):
            if kwargs["upload_photos"]:
                public_id = str(uuid.uuid4())
            else:
                public_id = image["public_id"]

            extension = os.path.splitext(image["filename"])[1]

            path_start = "pictures/" + datetime.datetime.utcnow().strftime("%Y/%m/%d/")

            if kwargs["upload_photos"]:
                bucket.upload_file(
                    str(pathlib.Path(kwargs["images_dir"], image["filename"])),
                    "media/" + path_start + public_id + extension,
                )
                photo = path_start + public_id + extension
            else:
                photo = image["photo"]

            picture = Picture.objects.create(
                public_id=public_id,
                title=image["title"],
                description="description",
                photo=photo,
                tags=" ".join(image["tags"]),
                uploaded_by=random.choice(users),
            )
            picture.save()

            if index % 50 == 0:
                print(index)
