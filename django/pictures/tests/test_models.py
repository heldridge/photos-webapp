from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture, Favorite, get_pictures
from users.models import CustomUser


class TestGetPictures(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_pictures = [
            {"title": "1", "tags": "a"},
            {"title": "2", "tags": "b"},
            {"title": "3", "tags": "c"},
            {"title": "4", "tags": "d"},
            {"title": "5", "tags": "e"},
        ]

        for picture in test_pictures:
            Picture.objects.create(
                title=picture["title"],
                description="Desc",
                tags=picture["tags"],
                photo=SimpleUploadedFile(
                    name="picture1.jpg",
                    content=open("test_data/picture1.jpg", "rb").read(),
                ),
            )

        test_users = [
            {"email": "a@x.com", "favorites": ["1", "4", "3", "5"]},
            {"email": "b@x.com", "favorites": ["1", "3", "5"]},
            {"email": "c@x.com", "favorites": ["3", "4"]},
            {"email": "d@x.com", "favorites": ["3", "5"]},
        ]
        for user in test_users:
            new_user = CustomUser.objects.create(email=user["email"])

            for favorite in user["favorites"]:
                Favorite.objects.create(
                    user=new_user, picture=Picture.objects.get(title=favorite)
                )

    def test_default_order(self):
        result = list(get_pictures(5))
        self.assertEqual(result[0].title, "5")

    def test_default_order_before(self):
        public_id = Picture.objects.get(title="3").public_id
        result = list(get_pictures(5, before=public_id))
        result.reverse()
        self.assertEqual([picture.title for picture in result], ["5", "4"])

    def test_default_order_after(self):
        public_id = Picture.objects.get(title="4").public_id
        result = list(get_pictures(5, after=public_id))
        self.assertEqual([picture.title for picture in result], ["3", "2", "1"])

    def test_favorites_order(self):
        result = list(get_pictures(5, order="most_favorites"))
        self.assertEqual(
            [picture.title for picture in result], ["3", "5", "4", "1", "2"]
        )

    def test_favorites_order_before(self):
        public_id = Picture.objects.get(title="1").public_id
        result = list(get_pictures(5, order="most_favorites", before=public_id))
        result.reverse()
        self.assertEqual([picture.title for picture in result], ["3", "5", "4"])

    def test_favorites_order_after(self):
        public_id = Picture.objects.get(title="4").public_id
        result = list(get_pictures(5, order="most_favorites", after=public_id))
        self.assertEqual([picture.title for picture in result], ["1", "2"])


"""
get the after picture's number of favs
fetch everything with favs leq than its number of favs
filter out anything with an id geq than its id
"""
