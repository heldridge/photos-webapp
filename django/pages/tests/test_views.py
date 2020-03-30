import uuid

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture
from users.models import CustomUser


class TestPagesLoad(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(email="test@example.com", password="test")

        num_pictures = 32
        for _ in range(num_pictures):
            Picture.objects.create(
                title="Test Title",
                description="Desc",
                tags="a b c d",
                photo=SimpleUploadedFile(
                    name="picture1.jpg",
                    content=open("test_data/picture1.jpg", "rb").read(),
                ),
                uploaded_by=cls.user,
            )

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_gallery(self):
        response = self.client.get("/gallery")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get("/search")
        self.assertEqual(response.status_code, 200)

    def test_search_with_tags(self):
        response = self.client.get("/search?q=b")
        self.assertEqual(response.status_code, 200)

    def test_search_with_before_after(self):
        mid_picture = Picture.objects.all()[16]
        response = self.client.get(f"/search?before={mid_picture.public_id}")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/search?after={mid_picture.public_id}")
        self.assertEqual(response.status_code, 200)

    def test_search_with_bad_before_after(self):
        response = self.client.get(f"/search?before={uuid.uuid4()}")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/search?after={uuid.uuid4()}")
        self.assertEqual(response.status_code, 200)

    def test_search_uploaded_by(self):
        response = self.client.get(f"/search?uploaded_by={self.user.public_id}")
        self.assertEqual(response.status_code, 200)

    def test_search_uploaded_by_bad_id(self):
        response = self.client.get(f"/search?uploaded_by={uuid.uuid4()}")
        self.assertEqual(response.status_code, 200)

    def test_search_with_favorites(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/search?favorites=true")
        self.assertEqual(response.status_code, 200)
