from django.shortcuts import render
from django.template import RequestContext, loader
import requests

class Mailgunner:
    """ This class is used to send emails using the requests module to the mailgun message api.
        NOTE: This class has the Python-Requests package as a dependency. 
        Run 'pip install requirements.txt' to install on your environment. """

    url = "https://api.mailgun.net/v3/mailgun.mcbella.com.ng/messages"
    auth = ("api", "key-e75e2753c478e22772ab5d30dc4171c4")

    @staticmethod
    def compose(sender, reciepient, subject, text="", html="None"):
        """RECOMMENDED: use this method to compose the email dict to use with send"""
        email = {
            "from": sender,
            "to": [reciepient,],
            "subject": subject,
            "text": text,
            "html": html
        }
        return email

    @staticmethod
    def send(email):
        """NOTE: email must be a dict"""
        try:
            status_code = requests.post( Mailgunner.url, auth=Mailgunner.auth, data=email ).status_code
        except:
            status_code = 520
        return status_code