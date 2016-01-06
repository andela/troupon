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


class UserchangePasswordTestCase(TestCase):

    '''Test that User can successfully change password.'''

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='johndoe',
                                             email='johndoe@gmail.com',
                                             password='12345')

    def test_user_can_changepassword(self):

        data = dict(current_password="12345", password1="andela", password2="andela")
        response = self.client.post("/account/change_password/", data)
        self.assertEqual(response.status_code, 302)


class ChangePasswordErrorTestCase(TestCase):

    ''' Test that change password error is caught.'''

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='johndoe',
                                             email='johndoe@gmail.com',
                                             password='12345')

    def test_user_mismatch_changepassword(self):

        data = dict(current_password="12345", password1="andela", password2="hhhjjh")
        response = self.client.post("/account/change_password/", data)
        self.assertEqual(response.status_code, 302)

    def test_no_data_on_changepassword(self):

        data = dict(current_password="12345", password1="", password2="")
        response = self.client.post("/account/change_password/", data)
        self.assertEqual(response.status_code, 302)

    def test_only_one_field_given_on_changepassword(self):

        data = dict(current_password="12345", password1="andela", password2="")
        response = self.client.post("/account/change_password/", data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_currentpassword(self):

        data = dict(current_password="wrong", password1="andela", password2="")
        response = self.client.post("/account/change_password/", data)
        self.assertEqual(response.status_code, 302)
