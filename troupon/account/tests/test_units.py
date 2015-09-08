from django.test import TestCase, Client
from django.contrib.auth.models import User as Account

from account.hashs import UserHasher as Hasher
from account.emails import Mailgunner


class AccountHashsTestCase(TestCase):
    """ This class tests the user account hash generation and hash reversing functions defined in the 'account.hashs'module.
        It tests the round trip: generating a unique hash for a user and then testing it against results of the reverse process"""
    
    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.registered_user = Account.objects.create_user('SamuelJames', 'samuel.james@andela.com', 'Django1491')
        self.registered_user.first_name = 'James'
        self.registered_user.last_name = 'Samuel'
        self.registered_user.save()


    def test_gen_hash_returns_min_50_chars(self):
        generated_hash = Hasher.gen_hash(self.registered_user)
        self.assertGreaterEqual(len(generated_hash), 50)


    def test_reverse_hash_returns_user_instance(self):
        generated_hash = Hasher.gen_hash(self.registered_user)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertIsInstance(reversed_hash_result, Account)


    def test_reverse_hash_returns_None_for_Wrong_hash(self):
        generated_hash = "a2374920910"
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(reversed_hash_result, None)


    def test_generated_hash_reverses_correctly(self):
        generated_hash = Hasher.gen_hash(self.registered_user)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(self.registered_user.pk, reversed_hash_result.pk)



class EmailTestCase(TestCase):
    
    def setUp(self):
        # compose test email:
        self.email =  Mailgunner.compose(
            sender = 'Troupon Tests <troupon@andela.com>',
            reciepient = 'awillionaire@gmail',
            subject = 'Troupon Email Integaration With Mailgun (Tests)',
            html = "<h1>Troupon ---> Mailgun API ---> You</h1><p>Testing Mic: 1, 2</p>",
            text = "Troupon ---> Mailgun API ---> You \n\nTesting Mic: 1, 2",
        )
    
    def test_send_email_returns_request_status(self):
        response = Mailgunner.send(self.email)
        self.assertGreaterEqual(response, 200)