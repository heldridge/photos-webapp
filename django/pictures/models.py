import io
import uuid

from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchVectorField
from django.core import exceptions
from django.core.files import File
from django.core.validators import RegexValidator
from django.utils.timezone import now

from PIL import Image

from users.models import CustomUser


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pictures/%Y/%m/%d/")
    tags = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r"^[a-zA-Z0-9- ]*$",
                "Tags must only contain characters lowercase a-z, numbers, and dashes (-)",
                code="invalid",
            )
        ],
    )
    uploaded_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Thumbnails
    thumbnail_w_272 = models.ImageField(
        upload_to="thumbnails/w272/%Y/%m/%d/", blank=True
    )

    # Note: be sure to update how this is done (trigger in postgres)
    # once django releases a good way to do Stored Generated Columns
    # https://stackoverflow.com/questions/59675402/django-full-text-searchvectorfield-obsolete-in-postgresql
    indexed_tags_search = SearchVectorField(null=True)

    uploaded_by = models.ForeignKey(CustomUser, models.SET_NULL, blank=True, null=True)

    class Meta:
        indexes = [GinIndex(fields=["indexed_tags_search"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail_w_272:
            self.thumbnail_w_272 = self.make_thumbnail(
                self.photo, (272, self.photo.height)
            )

    def make_thumbnail(self, image, size):
        """Makes thumbnails of given size from given image
        
        Args:
            image (``django.ImageField``): The image to generate a thumbnail for
            size (``tuple`` of ``int``): The width and height to generate

        Returns:
            ``django.File``: The resized image
        """
        image.open()
        im = Image.open(image)
        im.thumbnail(size)  # resize image

        thumb_io = io.BytesIO()  # create a BytesIO object

        im.save(thumb_io, "JPEG", quality=85)  # save image to BytesIO object

        thumbnail = File(
            thumb_io, name=image.name
        )  # create a django friendly File object

        return thumbnail

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
def get_pictures(
    amount,
    before=None,
    after=None,
    tags=[],
    favorited_by=None,
    uploaded_by=None,
    get_uploaded_by=False,
):
    """Queries the database or elasticsearch for pictures
    Args:
        amount (``int``): The number of pictures to return
        before (``str``): The id of the photo to fetch photos before
        after (``str``): The id of the photo to fetch photos after
        tags (``list`` of ``str``): The list of tags to search for
        uploaded_by (``user``): Limits pictures to only those uploaded by the user
        favorited_by (``user``):
            Limits pictures to only those favorited by the user
        get_uploaded_by (``bool``):
            Whether to pre-fetch the user that uploaded the image

    Returns:
        a ``QuerySet`` of pictures objects

    Raises:
        ``ValueError``: If both before and after are specified
    """
    # Normalize the values of before and after
    if before == "":
        before = None
    if after == "":
        after = None

    if before is not None and after is not None:
        raise ValueError("Only one of before and after can be specified")

    # Fetch the correct before or after picture
    if before is not None:
        try:
            # TODO: Change before and after fetching to use one trip to the database
            before_picture = Picture.objects.get(public_id=before)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            before = None
    if after is not None:
        try:
            after_picture = Picture.objects.get(public_id=after)
        except (exceptions.ValidationError, Picture.DoesNotExist):
            after = None

    query_set = Picture.objects

    if get_uploaded_by:
        query_set = query_set.select_related("uploaded_by")

    if favorited_by is not None:
        query_set = query_set.filter(favorite__user=favorited_by)

    if uploaded_by is not None:
        query_set = query_set.filter(uploaded_by=uploaded_by)

    if len(tags) > 0:
        query_set = query_set.filter(
            indexed_tags_search=SearchQuery(" ".join(tags), config="simple")
        )

    if before is not None:
        # For before we want to go "backwards," to get the pictures
        # closest in id to before_picture, so order by id (increasing)
        query_set = list(query_set.filter(id__gt=before_picture.id).order_by("id"))
    elif after is not None:
        query_set = query_set.filter(id__lt=after_picture.id).order_by("-id")
    else:
        query_set = query_set.order_by("-id")

    return query_set[:amount]
