import datetime
from unittest import mock

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pictures.models import Picture
from users.models import CustomUser
import users.views


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

        cls.user = CustomUser.objects.create(email="zirap@gmail.com", password="test")

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

    def test_send_email_not_logged_int(self):
        response = self.client.post("/accounts/send-confirmation-email")
        self.assertEqual(response.status_code, 401)

    def test_send_email_no_prev(self):
        users.views.send_mail = mock.Mock()
        self.client.force_login(self.user)
        response = self.client.post("/accounts/send-confirmation-email")
        self.assertEqual(response.status_code, 200)

    def test_send_mail_oldest_prev_okay(self):
        users.views.send_mail = mock.Mock()
        self.user.last_email_dates = [datetime.datetime.now().date()] * 4
        self.user.last_email_dates.append(datetime.date(2000, 1, 1))
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.post("/accounts/send-confirmation-email")

        self.assertEqual(response.status_code, 200)
        self.user.last_email_dates = []
        self.user.save()

    def test_send_mail_oldest_prev_bad(self):
        users.views.send_mail = mock.Mock()
        self.user.last_email_dates = [datetime.datetime.now().date()] * 5
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.post("/accounts/send-confirmation-email")

        self.assertEqual(response.status_code, 429)
        self.user.last_email_dates = []
        self.user.save()

    def test_email_shifts_dates(self):
        users.views.send_mail = mock.Mock()
        self.user.last_email_dates = [
            datetime.date(2000, 5, 5),
            datetime.date(2000, 4, 4),
            datetime.date(2000, 3, 3),
            datetime.date(2000, 2, 2),
            datetime.date(2000, 1, 1),
        ]
        self.user.save()

        self.client.force_login(self.user)
        self.client.post("/accounts/send-confirmation-email")

        self.assertEqual(
            CustomUser.objects.all()[0].last_email_dates,
            [
                datetime.datetime.utcnow().date(),
                datetime.date(2000, 5, 5),
                datetime.date(2000, 4, 4),
                datetime.date(2000, 3, 3),
                datetime.date(2000, 2, 2),
            ],
        )
