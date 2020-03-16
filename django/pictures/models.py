import datetime
import threading
import uuid

from django.db import models
from django.conf import settings
from django.core import exceptions
from django.contrib.postgres.fields import ArrayField
from sorl.thumbnail import get_thumbnail


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pictures/%Y/%m/%d/")
    tags = models.TextField(blank=True)
    uploaded_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # uploaded_by = ForeignKey
    # galleries = ForeignKey (many to many???)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for size in settings.THUMBNAIL_SIZES:
            thumbnail_creator = threading.Thread(
                target=get_thumbnail, args=(self.photo, size)
            )
            thumbnail_creator.start()

    # TODO: Will get called multiple times in template. Maybe persist when it is created?
    @property
    def split_tags(self):
        tags = str(self.tags).split()
        data = {"above_tags": [], "below_tags": []}

        max_width = 85  # Max width of the theoretical tag bar
        expander_length = 5  # Width of the "click to expand" symbol
        static_width_addition = 4  # How much to add in addition to each letter
        current_width = 0
        above = True
        # TODO: Minor optimization, stop adding once above is hit
        for tag in tags:
            current_width += static_width_addition + len(tag)
            if current_width + expander_length > max_width:
                above = False

            if above:
                data["above_tags"].append(tag)
            else:
                data["below_tags"].append(tag)
        return data


class Favorite(models.Model):
    class Meta:
        unique_together = (("user", "picture"),)

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    picture = models.ForeignKey("Picture", on_delete=models.CASCADE)


###################
# UTILITY METHODS #
###################
def get_pictures(amount, before=None, after=None, tags=[]):
    """Queries the database or elasticsearch for pictures
    Args:
        amount (``int``): The number of pictures to return
        before (``str``): The id of the photo to fetch photos before
        after (``str``): The id of the photo to fetch photos after
        tags (``list`` of ``str``): The list of tags to search for
    Returns:
        {
            "result": A list of pictures,
            "more_left": (``bool``) Whether there are more 
                         pictures remaining with the given query specification.
        }
    Raises:
        ``ValueError``: If both before and after are specified
    """
    if before is not None and after is not None:
        raise ValueError("Only one of before and after can be specified")

    # Fetch the correct before or after picture
    if before is not None and before != "":
        try:
            before_picture = Picture.objects.get(public_id=before)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            before = None
    if after is not None and after != "":
        try:
            after_picture = Picture.objects.get(public_id=after)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            after = None

    query_set = Picture.objects

    if len(tags) > 0:
        query_set = query_set.filter(tags__search=" ".join(tags))

    if before is not None:
        # For before we want to go "backwards," to get the pictures
        # closest in id to before_picture, so order by id (increasing)
        query_set = list(query_set.filter(id__gt=before_picture.id).order_by("id"))
    elif after is not None:
        query_set = query_set.filter(id__lt=after_picture.id).order_by("-id")
    else:
        query_set = query_set.order_by("-id")

    return query_set[:amount]
