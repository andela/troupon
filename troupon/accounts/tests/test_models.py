from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserProfile


class UserProfileModelTestCase(TestCase):
    """Testsuite for the Tickets model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@gmail.com',
            password='12345'
        )

    def test_can_create_read_update_userprofile(self):
        # test that user can create userProfile
        userprofile = UserProfile(
            user=self.user,
            country=2,
            location=84,
            occupation='Developer',
            phonenumber='08020202020',
            intlnumber='+12334567789'
        )
        userprofile.save()
        self.assertNotEqual(UserProfile.objects.count(), 0)

        # test that a userprofile record has been added
        userprofile = UserProfile.objects.get(id=userprofile.id)
        self.assertIsNotNone(userprofile.id)

        # update a userprofile record
        new_occupation = "Architect"
        another_userprofile = UserProfile.objects.get(id=userprofile.id)
        another_userprofile.occupation = new_occupation
        another_userprofile.save()

        # test that update has taken effect
        another_userprofile = UserProfile.objects.get(id=userprofile.id)
        self.assertEquals(another_userprofile.occupation, new_occupation)

        # delete a userprofile record
        another_userprofile = UserProfile.objects.get(id=userprofile.id)
        UserProfile.delete(another_userprofile)
        with self.assertRaises(UserProfile.DoesNotExist) as context:
            UserProfile.objects.get(id=userprofile.id)
        self.assertTrue("does not exist" in context.exception.message)
