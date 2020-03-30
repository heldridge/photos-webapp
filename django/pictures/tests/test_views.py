import uuid

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture


class TestPagesLoad(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_pictures = 1
        for _ in range(num_pictures):
            Picture.objects.create(
                title="Test Title",
                description="Desc",
                tags="a b c d",
                photo=SimpleUploadedFile(
                    name="picture1.jpg",
                    content=open("test_data/picture1.jpg", "rb").read(),
                ),
            )

    def test_upload(self):
        response = self.client.get("/pictures/upload")
        self.assertEqual(response.status_code, 200)

    def test_picture(self):
        public_id = Picture.objects.all()[0].public_id
        response = self.client.get(f"/pictures/{public_id}")
        self.assertEqual(response.status_code, 200)

    def test_picture_wrong_uuid(self):
        response = self.client.get(f"/pictures/{uuid.uuid4()}")
        self.assertEqual(response.status_code, 200)

    def test_picture_bad_uuid(self):
        response = self.client.get(f"/pictures/bad")
        self.assertEqual(response.status_code, 200)
