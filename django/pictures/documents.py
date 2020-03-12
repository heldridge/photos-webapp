# documents.py
from django.core import exceptions

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Picture


@registry.register_document
class PictureDocument(Document):
    tags = fields.KeywordField()
    public_id = fields.TextField()
    photo = fields.TextField()

    def prepare_public_id(self, instance):
        return str(instance.public_id)

    def prepare_photo(self, instance):
        return str(instance.photo)

    class Index:
        # Name of the Elasticsearch index
        name = "pictures"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Picture  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "id",
            "title",
            "description",
            "uploaded_at",
            "updated_at",
        ]


def get_pictures(amount, before=None, after=None, tags=None):
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

    # If tags is None we can get everything from the database
    if tags is None:
        query_set = Picture.objects
        if before is not None:
            # For before we want to go "backwards," to get the pictures
            # closest in id to before_picture, so order by id (increasing)
            query_set = list(query_set.filter(id__gt=before_picture.id).order_by("id"))
        elif after is not None:
            query_set = query_set.filter(id__lt=after_picture.id).order_by("-id")
        else:
            query_set = query_set.order_by("-id")

    # If there are tags we have to go to Elasticsearch
    else:
        query_set = PictureDocument.search()

        for tag in tags:
            query_set = query_set.query("term", tags=tag)

        if before is not None:
            query_set = query_set.query("range", id={"gt": before_picture.id}).sort(
                "id"
            )
        elif after is not None:
            query_set = query_set.query("range", id={"lt": after_picture.id}).sort(
                "-id"
            )
        else:
            query_set = query_set.sort("-id")

    query_set = query_set[: amount + 1]

    # We went "backwards" if we had a before, so reverse the list now
    if before is not None:
        query_set.reverse()

    return {"pictures": query_set[:amount], "more_left": len(query_set) < amount + 1}
