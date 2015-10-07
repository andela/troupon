from django.shortcuts import render
from django.template import RequestContext, loader
import requests
import os

class Mailgunner:
    """ This class is used to send emails using the requests module to the mailgun message api.
        NOTE: This class has the Python-Requests package as a dependency. 
        Run 'pip install requirements.txt' to install on your environment. """

    url = os.getenv('MAILGUN_URL')
    auth = (os.getenv('MAILGUN_USERNAME'), os.getenv('MAILGUN_PASSWORD'))

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
            status_code = requests.post( Mailgunner.url, auth=Mailgunner.auth, data=email).status_code
        except:
            status_code = 520
        return status_code