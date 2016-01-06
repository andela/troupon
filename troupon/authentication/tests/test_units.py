from django.test import TestCase, Client
from django.contrib.auth.models import User

from authentication.hashs import UserHasher as Hasher
from authentication.emails import SendGrid


class HashsTestCase(TestCase):
    """
    This class tests the user authentication hash generation and hash
    reversing functions defined in the 'authentication.hashs' module.
    It tests the round trip: generating a unique hash for a user
    and then testing it against results of the reverse process.
    """

    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.user = User(
            username='JohnDoe',
            email='johndoe@somedomain.com',
            first_name='John',
            last_name='Doe'
        )
        self.user.set_password('notsosecret12345')
        self.user.save()

    def test_gen_hash_returns_min_50_chars(self):
        generated_hash = Hasher.gen_hash(self.user)
        self.assertGreaterEqual(len(generated_hash), 50)

    def test_reverse_hash_returns_user_instance(self):
        generated_hash = Hasher.gen_hash(self.user)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertIsInstance(reversed_hash_result, User)

    def test_reverse_hash_returns_None_for_Wrong_hash(self):
        generated_hash = "a2374920910"
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(reversed_hash_result, None)

    def test_generated_hash_reverses_correctly(self):
        generated_hash = Hasher.gen_hash(self.user)
        reversed_hash_result = Hasher.reverse_hash(generated_hash)
        self.assertEquals(self.user.pk, reversed_hash_result.pk)


class EmailTestCase(TestCase):

    def setUp(self):
        # compose test email:
        self.email = SendGrid.compose(
            sender='Troupon Tests <troupon@andela.com>',
            recipient='johndoe@somedomain.com',
            subject='Troupon Email Integaration With SendGrid (Tests)',
            html="<h1>Troupon ---> SendGrid API ---> You\
            </h1><p>Testing Mic: 1, 2</p>",
            text="Troupon ---> SendGrid API ---> You \n\nTesting Mic: 1, 2"
        )

    def test_sendgrid_sends_email(self):

        response = SendGrid.send(self.email)
        self.assertEquals(200, response)
