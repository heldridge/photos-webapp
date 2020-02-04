import datetime
import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pictures/%Y/%m/%d/")
    tags = ArrayField(models.CharField(max_length=20), blank=True)
    # uploaded_by = ForeignKey
    uploaded_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # galleries = ForeignKey (many to many???)

    def __str__(self):
        return self.title
