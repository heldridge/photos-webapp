import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/user_uploads/')
    tags = ArrayField(models.CharField(max_length=20))
    # uploaded_by = ForeignKey
    uploaded_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    # galleries = ForeignKey (many to many???)

    def __str__(self):
        return self.title


"""
{"id": 0, "title": "Blue Cone", "description": "", "filename": "aaa.jpg", "tags": ["food", "blue", "dessert", "ice-cream"], "uploaded_by": "admin", "uploaded_at": 1560894129000, "updated_at": 1560894129000, "galleries": []}
"""