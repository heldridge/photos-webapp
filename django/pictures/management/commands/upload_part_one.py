import datetime
import json
import os
import pathlib
import uuid

import boto3
from PIL import Image

from django.core.management.base import BaseCommand

# This should get everything into s3, and spit out the json to feed to upload part two.


class Command(BaseCommand):
    help = "Loads pictures into s3, to match upload_part_two which is run on the server"

    def add_arguments(self, parser):
        parser.add_argument("data_file", help="The path to the json file to load")
        parser.add_argument(
            "images_dir", help="The path to the directory holding the images"
        )
        parser.add_argument(
            "--limit", type=int, help="Limit the number of images loaded"
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="If added does not upload to s3"
        )
        parser.add_argument(
            "--output_file",
            default="out.json",
            help="Where to output the json for upload_part_two",
        )

    def handle(self, *args, **kwargs):
        with open(kwargs["data_file"], "r") as infile:
            data = json.load(infile)

        if kwargs["limit"]:
            data = data[: kwargs["limit"]]

        s3 = boto3.resource("s3")
        bucket = s3.Bucket("media.qlbhmmvpym.club")

        timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d/")
        path_start = "pictures/" + timestamp
        path_start_thumb = "thumbnails/w272/" + timestamp

        pathlib.Path(os.path.join(kwargs["images_dir"], "thumbnails")).mkdir(
            parents=True, exist_ok=True
        )

        for index, picture in enumerate(data):
            if index % 50 == 0:
                print(index)

            public_id = str(uuid.uuid4())
            extension = os.path.splitext(picture["filename"])[1]

            im = Image.open(os.path.join(kwargs["images_dir"], picture["filename"]))
            _, original_height = im.size

            im.thumbnail((272, original_height))

            with open(
                os.path.join(kwargs["images_dir"], "thumbnails", public_id + extension),
                "w+",
            ) as outfile:
                im.save(outfile, "JPEG", quality=85)

            if not kwargs["dry_run"]:
                bucket.upload_file(
                    os.path.join(kwargs["images_dir"], picture["filename"]),
                    "media/" + path_start + public_id + extension,
                )
                bucket.upload_file(
                    os.path.join(
                        kwargs["images_dir"], "thumbnails", public_id + extension
                    ),
                    "media/" + path_start_thumb + public_id + extension,
                )

            picture["public_id"] = public_id
            picture["photo"] = path_start + public_id + extension
            picture["thumbnail_w_272"] = path_start_thumb + public_id + extension
            del picture["filename"]

        with open(kwargs["output_file"], "w+") as outfile:
            json.dump(data, outfile, indent=2)
