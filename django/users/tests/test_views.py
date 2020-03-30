from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture
from users.models import CustomUser


class TestPagesLoad(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_pictures = 4
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

        cls.user = CustomUser.objects.create(email="test@example.com", password="test")

    def test_profile(self):
        self.client.force_login(self.user)
        response = self.client.get("/accounts/profile")
        self.assertEqual(response.status_code, 200)

    def test_profile_not_logged_in(self):
        response = self.client.get("/accounts/profile")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get("/accounts/register")
        self.assertEqual(response.status_code, 200)

    def test_settings(self):
        self.client.force_login(self.user)
        response = self.client.get("/accounts/profile/settings")
        self.assertEqual(response.status_code, 200)

    def test_settings_not_logged_in(self):
        response = self.client.get("/accounts/profile/settings")
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.get(f"/accounts/users/{self.user.public_id}")
        self.assertEqual(response.status_code, 200)
