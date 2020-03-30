from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture


class TestPagesLoad(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_pictures = 32
        for i in range(num_pictures):
            Picture.objects.create(
                title="Test Title",
                description="Desc",
                tags="a b c d",
                photo=SimpleUploadedFile(
                    name="picture1.jpg",
                    content=open("test_data/picture1.jpg", "rb").read(),
                ),
            )

    def test_my_worky(self):
        self.assertTrue(True)
