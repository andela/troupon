from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory

from accounts.models import UserProfile
from merchant.models import Merchant


class UserProfileMerchantTestCase(TestCase):

    def setUp(self):
        """
        User calls profile page.
        """
        self.client = Client()
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@gmail.com',
            password='12345'
        )
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            country=2,
            location=84,
            occupation='Developer',
            phonenumber='08020202020',
            intlnumber='+12334567789'
        )

        self.merchant = Merchant.objects.create(
            name='yourname',
            country=2,
            location=84,
            telephone='12345678901',
            intlnumber='+2342345678901',
            email='youremail',
            address='youraddress',
            slug='yourslug',
            userprofile=self.userprofile
        )

        self.superuser = User.objects.create_superuser(
            username='troupon_admin',
            email='admin@troupon.com',
            password='12345')

        self.client.login(username='johndoe', password='12345')


class UserProfileTestCase(TestCase):

    def setUp(self):
        """
        User calls profile page.
        """
        self.client = Client()
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@gmail.com',
            password='12345'
        )
        self.superuser = User.objects.create_superuser(
            username='troupon_admin',
            email='admin@troupon.com',
            password='12345')

        self.client.login(username='johndoe', password='12345')


class TestProfileAction(UserProfileTestCase):

    def test_user_default_account_page(self):

        response = self.client.get("/account/")
        self.assertEquals(response.status_code, 200)

    def test_user_account_profile_page(self):

        response = self.client.get("/account/profile/")
        self.assertEquals(response.status_code, 200)


class UserchangePasswordTestCase(TestCase):

    '''Test that User can successfully change password.'''

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='johndoe',
                                             email='johndoe@gmail.com',
                                             password='12345')

    def test_user_can_changepassword(self):

        data = dict(current_password="12345",
                    password1="andela",
                    password2="andela")

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

        data = dict(
            current_password="12345",
            password1="andela",
            password2="hhhjjh"
        )

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
