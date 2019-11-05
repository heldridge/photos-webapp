from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=20))
    photo = models.ImageField(upload_to='photos/user_uploads/')

    def __str__(self):
        return self.title
