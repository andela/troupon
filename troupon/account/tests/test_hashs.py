from django.test import TestCase, Client
from django.contrib.auth.models import User as UserAccount
from account.hashs import UserHashUtils

class AccountHashsTestCase(TestCase):
    """ This class tests the user account hash generation and hash reversing functions defined in the 'account.hashs'module.
        It tests the round trip: generating a unique hash for a user and then testing it against results of the reverse process"""
    
    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a smaple user:
        self.registered_account = UserAccount.objects.create_user('AwiliUzo', 'awillionaire@gmail.com', 'Young1491')
        self.registered_account.first_name = 'Uzo'
        self.registered_account.last_name = 'Awili'
        self.registered_account.save()

        # get an intsance of self.hasher
        self.hasher = UserHashUtils()

    def test_gen_hash_returns_min_50_chars(self):
        generated_user_hash = self.hasher.gen_hash(self.registered_account)
        self.assertGreaterEqual(len(generated_user_hash), 50)

    def test_reverse_hash_returns_user_instance(self):
        generated_user_hash = self.hasher.gen_hash(self.registered_account)
        reversed_user_hash_result = self.hasher.reverse_hash(self.generated_user_hash)
        self.assertIsInstance(reversed_user_hash_result, UserAccount)

    def test_reverse_hash_returns_None_for_Wrong_hash(self):
        generated_user_hash = "a2374920910"
        reversed_user_hash_result = self.hasher.reverse_hash(self.generated_user_hash)
        self.assertEquals(reversed_user_hash_result, None)

    def test_generated_hash_reverses_correctly(self):
        generated_user_hash = self.hasher.gen_hash(self.registered_account)
        reversed_user_hash_result = self.hasher.reverse_hash(self.generated_user_hash)
        self.assertEquals(self.registered_account.id, reversed_user_hash_result.id)