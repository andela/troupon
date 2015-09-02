from django.test import TestCase, Client
from django.contrib.auth.models import User as Account
from account.hashs import UserHashUtils as Hasher

class AccountHashsTestCase(TestCase):
    """ This class tests the user account hash generation and hash reversing functions defined in the 'account.hashs'module.
        It tests the round trip: generating a unique hash for a user and then testing it against results of the reverse process"""
    
    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.registered_account = Account.objects.create_user('AwiliUzo', 'awillionaire@gmail.com', 'Young1491')
        self.registered_account.first_name = 'Uzo'
        self.registered_account.last_name = 'Awili'
        self.registered_account.save()


    def test_gen_hash_returns_min_50_chars(self):
        generated_hash = Hasher.gen_hash(self.registered_account)
        self.assertGreaterEqual(len(generated_hash), 50)


    def test_reverse_hash_returns_user_instance(self):
        generated_hash = Hasher.gen_hash(self.registered_account)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertIsInstance(reversed_hash_result, Account)


    def test_reverse_hash_returns_None_for_Wrong_hash(self):
        generated_hash = "a2374920910"
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(reversed_hash_result, None)


    def test_generated_hash_reverses_correctly(self):
        generated_hash = Hasher.gen_hash(self.registered_account)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(self.registered_account.pk, reversed_hash_result.pk)
        # self.assertEquals(self.registered_account.pk, 1)