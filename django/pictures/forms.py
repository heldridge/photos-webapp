from django import forms

from .models import Picture


class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["title", "photo", "tags"]
