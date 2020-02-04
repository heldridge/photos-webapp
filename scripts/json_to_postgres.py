import argparse
import datetime
import json
import logging
import uuid

import psycopg2


# Set up logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def format_tags(tags):
    if tags:
        formatted = "{"
        for tag in tags:
            formatted += '"' + tag + '", '

        return formatted[:-2] + "}"
    else:
        return "{}"


def format_timestamp(timestamp):
    tz = datetime.datetime.fromtimestamp(timestamp / 1000).strftime("%c")
    return tz + " z"


def format_title(title):
    return title.replace("'", "''")


def main():
    django_password = open("../secrets/postgres_django_password.txt", "r").read()

    parser = argparse.ArgumentParser(
        description=(
            "Take information from a json file and upload it " "to a postgres db"
        )
    )
    parser.add_argument("--db", help="The name of the database", default="photos")
    parser.add_argument("--user", help="The user to connect as", default="django")
    parser.add_argument(
        "--password", help="the password to connect with", default=django_password
    )
    parser.add_argument(
        "--data_file",
        help="The json file containing the data to upload",
        default="../../data/pictures.json",
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable verbose logging", action="store_true"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    with open(args.data_file, "r") as infile:
        data = json.load(infile)

    for image in data:
        conn = psycopg2.connect(
            host="localhost", database=args.db, user=args.user, password=args.password
        )

        try:
            logger.info("Inserting %s %s", image["id"], image["title"])
            sql = (
                f"INSERT INTO pictures_picture VALUES "
                f"("
                f"{image['id']}, "  # id
                f"'{format_title(image['title'])}', "  # title
                f"'description', "  # description
                f"'pictures/2020/01/01/{image['filename']}', "  # photo
                f"'{format_tags(image['tags'])}', "  # tags
                f"'{format_timestamp(image['uploaded_at'])}', "  # uploaded_at
                f"'{format_timestamp(image['updated_at'])}', "  # updated_at
                f"'{str(uuid.uuid4())}'"  # public_id
                f")"
            )
            logger.debug("Executing query: %s", sql)

            try:
                cur = conn.cursor()
                cur.execute(sql)
            except psycopg2.errors.UniqueViolation:
                logger.warning("Skipping due to duplicate id %d", image["id"])

        except (Exception, psycopg2.DatabaseError):
            logger.exception("Something went wrong")
            if conn is not None:
                conn.close()
            break

        conn.commit()
        conn.close()


if __name__ == "__main__":
    main()


"""
 id          | integer                  |           | not null | nextval('pictures_picture_id_seq'::regclass)
 title       | character varying(100)   |           | not null |
 description | text                     |           | not null |
 photo       | character varying(100)   |           | not null |
 tags        | character varying(20)[]  |           | not null |
 uploaded_at | timestamp with time zone |           | not null |
 updated_at  | timestamp with time zone |           | not null |
 public_id   | uuid                     |           | not null |
 """
