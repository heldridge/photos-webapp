import argparse
import os

import boto3


def main():
    parser = argparse.ArgumentParser(description="Uploads media files to s3")
    parser.add_argument(
        "folder", help="The root media folder to upload (without the /media/ prefix"
    )
    parser.add_argument("bucket", help="The name of the s3 bucket to upload to")
    args = parser.parse_args()

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(args.bucket)

    start_of_path = os.path.basename(os.path.normpath(args.folder))
    part_of_path_to_remove = args.folder[: -len(start_of_path)]

    for path_list in os.walk(args.folder):
        base_path = path_list[0][len(part_of_path_to_remove) :]
        for filename in path_list[2]:
            bucket.upload_file(
                os.path.join(path_list[0], filename),
                os.path.join("media", base_path, filename),
            )


if __name__ == "__main__":
    main()

