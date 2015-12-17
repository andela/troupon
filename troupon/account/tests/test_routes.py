from django.test import TestCase, Client
from django.contrib.auth.models import User


class UserProfileTestCase(TestCase):

    def setUp(self):
        """
        User calls profile page.
        """
        self.client_stub = Client()

        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@gmail.com',
            password='12345'
        )

    def test_user_default_account_page(self):

        response = self.client_stub.get("/account/")
        self.assertEquals(response.status_code, 302)

    def test_user_account_profile_page(self):

        response = self.client_stub.get("/account/profile/")
        self.assertEquals(response.status_code, 302)

    def test_user_account_merchant_view(self):

        response = self.client_stub.get("/account/merchant/")
        self.assertEquals(response.status_code, 302)
