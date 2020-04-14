from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture, Favorite, get_pictures, shorten_number
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

    def test_only_favs_favorites_order(self):
        faved_by = CustomUser.objects.get(email="a@x.com")
        result = list(get_pictures(16, favorited_by=faved_by, order="most_favorites"))
        self.assertEqual([picture.title for picture in result], ["3", "5", "4", "1"])


class TestShortenNumber(TestCase):
    def test_no_change(self):
        self.assertEqual(shorten_number(0), "0")
        self.assertEqual(shorten_number(1), "1")
        self.assertEqual(shorten_number(7), "7")
        self.assertEqual(shorten_number(23), "23")
        self.assertEqual(shorten_number(105), "105")
        self.assertEqual(shorten_number(500), "500")
        self.assertEqual(shorten_number(999), "999")

    def test_four_digit(self):
        self.assertEqual(shorten_number(1000), "1k")

        self.assertEqual(shorten_number(1001), "1k")
        self.assertEqual(shorten_number(1099), "1k")
        self.assertEqual(shorten_number(1100), "1.1k")
        self.assertEqual(shorten_number(1999), "1.9k")
        self.assertEqual(shorten_number(2358), "2.3k")
        self.assertEqual(shorten_number(7006), "7k")
        self.assertEqual(shorten_number(9999), "9.9k")

    def test_five_digit(self):
        self.assertEqual(shorten_number(10000), "10k")
        self.assertEqual(shorten_number(10050), "10k")
        self.assertEqual(shorten_number(10099), "10k")
        self.assertEqual(shorten_number(10100), "10.1k")
        self.assertEqual(shorten_number(15699), "15.6k")
        self.assertEqual(shorten_number(99999), "99.9k")

    def test_larger_digits(self):
        self.assertEqual(shorten_number(474621), "474k")
        self.assertEqual(shorten_number(1875639), "1.8m")
        self.assertEqual(shorten_number(74637299), "74.6m")
        self.assertEqual(shorten_number(643029278), "643m")
        self.assertEqual(shorten_number(76487439440), ">1b")
