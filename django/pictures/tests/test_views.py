import json
import uuid

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture, Favorite, Tag
from users.models import CustomUser


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

    def test_tags(self):
        response = self.client.get("/pictures/tags/")
        self.assertEqual(response.status_code, 200)

    def test_tags_letter(self):
        response = self.client.get("/pictures/tags?letter=b")
        self.assertEqual(response.status_code, 200)

    def test_tags_page(self):
        response = self.client.get("/pictures/tags?page=2")
        self.assertEqual(response.status_code, 200)


class TestFavorites(TestCase):
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

        cls.picture = Picture.objects.all()[0]

        cls.user = CustomUser.objects.create(email="test@example.com", password="test")

    def test_add_favorite(self):
        self.client.force_login(self.user)
        response = self.client.post(f"/pictures/{self.picture.public_id}/favorites/")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Favorite.objects.filter(picture=self.picture, user=self.user).exists()
        )

    def test_add_favorite_not_logged_in(self):
        response = self.client.post(f"/pictures/{self.picture.public_id}/favorites/")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(len(Favorite.objects.all()) == 0)

    def test_delete_favorite(self):
        self.client.force_login(self.user)
        self.client.post(f"/pictures/{self.picture.public_id}/favorites/")
        self.client.delete(f"/pictures/{self.picture.public_id}/favorites/")
        self.assertTrue(len(Favorite.objects.all()) == 0)


class TestPictureViewContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(email="test@example.com", password="test")
        cls.user2 = CustomUser.objects.create(
            email="test2@example.com", password="test2"
        )
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
                uploaded_by=cls.user,
            )

    def test_no_delete_button_if_not_logged_in(self):
        public_id = Picture.objects.all()[0].public_id
        response = self.client.get(f"/pictures/{public_id}")
        self.assertNotContains(response, "deleteButton")

    def test_has_delete_when_logged_in(self):
        self.client.force_login(self.user)
        public_id = Picture.objects.all()[0].public_id
        response = self.client.get(f"/pictures/{public_id}")
        self.assertContains(response, "deleteButton")

    def test_no_delete_if_not_uploader(self):
        self.client.force_login(self.user2)
        public_id = Picture.objects.all()[0].public_id
        response = self.client.get(f"/pictures/{public_id}")
        self.assertNotContains(response, "deleteButton")

    def test_non_logged_in_delete_returns_401(self):
        public_id = Picture.objects.all()[0].public_id
        response = self.client.delete(f"/pictures/{public_id}")
        self.assertEqual(response.status_code, 401)

    def test_bad_id_not_found(self):
        self.client.force_login(self.user2)
        response = self.client.delete(f"/pictures/{uuid.uuid4()}")
        self.assertEqual(response.status_code, 404)

    def test_wrong_user_delete_returns_403(self):
        self.client.force_login(self.user2)
        public_id = Picture.objects.all()[0].public_id
        response = self.client.delete(f"/pictures/{public_id}")
        self.assertEqual(response.status_code, 403)

    def test_delete_picture(self):
        self.client.force_login(self.user)
        public_id = Picture.objects.all()[0].public_id
        response = self.client.delete(f"/pictures/{public_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Picture.objects.all()), 0)


class TestTags(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(201):
            Tag.objects.create(title=str(i), count=-1 * i)

    def test_tags_bad_page(self):
        response = self.client.get("/pictures/tags?page=bad")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["tags"], [])
        self.assertFalse(json.loads(response.content)["more_left"])

    def test_offset(self):
        response = self.client.get("/pictures/tags?page=2")
        data = json.loads(response.content)
        self.assertEqual(data["tags"][0]["title"], "50")
        self.assertEqual(data["tags"][-1]["title"], "99")
        self.assertTrue(data["more_left"])

    def test_small_amount(self):
        response = self.client.get("/pictures/tags?page=5")
        self.assertEqual(json.loads(response.content)["tags"][0]["title"], "200")
        self.assertFalse(json.loads(response.content)["more_left"])

    def test_too_large(self):
        response = self.client.get("/pictures/tags?page=10")
        self.assertEqual(len(json.loads(response.content)["tags"]), 0)
        self.assertFalse(json.loads(response.content)["more_left"])

    def test_negative_page(self):
        response = self.client.get("/pictures/tags?page=-1")
        self.assertEqual(len(json.loads(response.content)["tags"]), 0)
        self.assertFalse(json.loads(response.content)["more_left"])
