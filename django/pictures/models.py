import datetime
import threading
import uuid

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from sorl.thumbnail import get_thumbnail


class Tag(models.Model):
    title = models.CharField(max_length=20)


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pictures/%Y/%m/%d/")
    tags = models.ManyToManyField(Tag)
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


class Favorite(models.Model):
    class Meta:
        unique_together = (("user", "picture"),)

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    picture = models.ForeignKey("Picture", on_delete=models.CASCADE)


###################
# UTILITY METHODS #
###################
def normalize_photo(picture):
    """
    Normalizes the 'photo' field for Picture Models and Documents

    The Picture Model and the Picture Document handle the 'photo' field
    differently, which can lead to trickyness down the road.
    This method normalizes that field so that it is consistent.

    Args:
        picture (``str`` or ``ImageField``): the field value to normalize

    Returns:
        ``str``: the str value of the photo's filename
    """
    return str(picture.photo)


def get_split_tags(tags):
    """
    Splits an image's tags into "above" and "below" tags,
    so they don't over-clutter the UI

    Above and below are decided by estimating how wide
    the resulting tag bar would be, and then putting a cap on
    that width
    """
    data = {"above_tags": [], "below_tags": []}

    max_width = 85  # Max width of the theoretical tag bar
    expander_length = 5  # Width of the "click to expand" symbol
    static_width_addition = 4  # How much to add in addition to each letter
    current_width = 0
    above = True
    for tag in tags:
        current_width += static_width_addition + len(tag)
        if current_width + expander_length > max_width:
            above = False

        if above:
            data["above_tags"].append(tag)
        else:
            data["below_tags"].append(tag)
    return data

