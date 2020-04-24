import argparse
import datetime
import json
import os
import pathlib
import uuid

import boto3
from PIL import Image

# Setup arguments
parser = argparse.ArgumentParser()
parser.add_argument("data_file", help="The path to the json file to load")
parser.add_argument("images_dir", help="The path to the directory holding the images")
parser.add_argument("--limit", type=int, help="Limit the number of images loaded")
parser.add_argument(
    "--dry-run", action="store_true", help="If added does not upload to s3"
)
parser.add_argument(
    "--output_file",
    default="out.json",
    help="Where to output the json for upload_part_two",
)
parser.add_argument(
    "--filename_attr",
    default="filename",
    help="The json attribute with the picture's filename",
)
args = parser.parse_args()


with open(args.data_file, "r") as infile:
    data = json.load(infile)

if args.limit:
    data = data[: args.limit]

s3 = boto3.resource("s3")
bucket = s3.Bucket("media.qlbhmmvpym.club")

timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d/")
path_start = "pictures/" + timestamp
path_start_thumb = "thumbnails/w272/" + timestamp

pathlib.Path(os.path.join(args.images_dir, "thumbnails")).mkdir(
    parents=True, exist_ok=True
)

for index, picture in enumerate(data):
    if index % 50 == 0:
        print(index)

    public_id = str(uuid.uuid4())
    extension = os.path.splitext(picture[args.filename_att])[1]

    im = Image.open(os.path.join(args.images_dir, picture[args.filename_att]))
    _, original_height = im.size

    im.thumbnail((272, original_height))

    with open(
        os.path.join(args.images_dir, "thumbnails", public_id + extension), "w+",
    ) as outfile:
        im.save(outfile, "JPEG", quality=85)

    if not args.dry_run:
        bucket.upload_file(
            os.path.join(args.images_dir, picture[args.filename_att]),
            "media/" + path_start + public_id + extension,
        )
        bucket.upload_file(
            os.path.join(args.images_dir, "thumbnails", public_id + extension),
            "media/" + path_start_thumb + public_id + extension,
        )

    picture["public_id"] = public_id
    picture["photo"] = path_start + public_id + extension
    picture["thumbnail_w_272"] = path_start_thumb + public_id + extension
    del picture[args.filename_att]

with open(args.output_file, "w+") as outfile:
    json.dump(data, outfile, indent=2)
