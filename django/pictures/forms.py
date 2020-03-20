from django import forms
from django.conf import settings

from .models import Picture


class PictureUploadForm(forms.ModelForm):
    error_css_class = "border-error"

    class Meta:
        model = Picture
        fields = ["title", "tags", "photo"]
        widgets = {
            "tags": forms.Textarea(attrs={"cols": 20, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": " ".join(settings.FORM_FIELD_CLASSES),}
        )
        self.fields["tags"].widget.attrs.update(
            {"class": " ".join(settings.FORM_FIELD_CLASSES),}
        )

    def is_valid(self):
        ret = super().is_valid()
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {
                    "class": " ".join(settings.FORM_FIELD_CLASSES)
                    + " "
                    + " ".join(settings.FORM_FIELD_ERROR_CLASSES),
                    "onfocus": "removeErrorBorder(this)",
                }
            )
        return ret
