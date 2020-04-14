import collections

from django.core.management.base import BaseCommand
from pictures.models import Picture, Tag


class Command(BaseCommand):
    help = "Updates the tags table based on all the tags in the pictures table"

    def handle(self, *args, **kwargs):

        tags = set()

        counter = collections.Counter()
        for tags in [picture.tags for picture in Picture.objects.all()]:
            counter.update(tags.split())
            tags.update(tags.split())

        progress = 0
        for title, count in dict(counter).items():
            tag, _ = Tag.objects.get_or_create(title=title)
            tag.count = count
            tag.save()
            progress += 1
            if progress % 50 == 0:
                print(progress)

        for tag in Tag.objects.all():
            if tag.title not in tags:
                tag.delete()
