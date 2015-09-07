from django.test import TestCase
from account.emails import Mailgunner

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
