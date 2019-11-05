import argparse
import datetime
import json
import logging

import psycopg2


# Set up logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def format_tags(tags):
    if tags:
        formatted = '{'
        for tag in tags:
            formatted += '"' + tag + '", '

        return formatted[:-2] + '}'
    else:
        return '{}'

def format_timestamp(timestamp):
    tz = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%c')
    return tz + ' z'

def format_title(title):
    return title.replace("'", "''")


def main():
    django_password = open(
        '../secrets/postgres_django_password.txt', 'r').read()

    parser = argparse.ArgumentParser(
        description=(
            'Take information from a json file and upload it '
            'to a postgres db'))
    parser.add_argument(
        '--db', help='The name of the database', default='photos')
    parser.add_argument(
        '--user', help='The user to connect as', default='django')
    parser.add_argument(
        '--password',
        help='the password to connect with',
        default=django_password)
    parser.add_argument(
        '--data_file',
        help='The json file containing the data to upload',
        default='../../data/pictures.json')
    parser.add_argument(
        '-v', '--verbose', help='Enable verbose logging', action='store_true')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    with open(args.data_file, 'r') as infile:
        data = json.load(infile)

    for image in data:
        conn = psycopg2.connect(
            host='localhost',
            database=args.db,
            user=args.user,
            password=args.password)

        try:
            logger.info('Inserting %s %s', image['id'], image['title'])
            sql = (f"INSERT INTO pictures_picture VALUES "
                   f"({image['id']}, '{format_title(image['title'])}', "
                   f"'{format_tags(image['tags'])}', "
                   f"'user_uploads/{image['filename']}', "
                   f"'description', '{format_timestamp(image['updated_at'])}', "
                   f"'{format_timestamp(image['uploaded_at'])}')")
            logger.debug('Executing query: %s', sql)

            try:
                cur = conn.cursor()
                cur.execute(sql)
            except psycopg2.errors.UniqueViolation:
                logger.warning('Skipping due to duplicate id %d', image['id'])

        except (Exception, psycopg2.DatabaseError):
            logger.exception("Something went wrong")
            if conn is not None:
                conn.close()
            break

        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()
