# documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Picture


@registry.register_document
class PictureDocument(Document):
    tags = fields.KeywordField()

    class Index:
        # Name of the Elasticsearch index
        name = "pictures"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Picture  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ["id", "title", "description", "photo", "uploaded_at", "updated_at"]
