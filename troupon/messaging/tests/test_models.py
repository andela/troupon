
from ..models import Message
from django.test import TestCase
from django.contrib.auth.models import User


class MessageTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(MessageTestCase, cls).setUpClass()
        cls.user1 = User.objects.create_user(
            'user1', 'user1@example.com', '123456')
        cls.user2 = User.objects.create_user(
            'user2', 'user2@example.com', '123456')
        cls.msg1 = Message(sender=cls.user1, recipient=cls.user2,
                           subject='Subject Text', body='Body Text')
        cls.msg1.save()

    def test_that_messages_can_be_created(self):
        """ Tests that messages can be created
        """
        pass

    def test_that_messages_can_be_read(self):
        """ Tests that messages can be read
        """
        pass

    def test_that_messages_can_be_replied_to(self):
        """ Tests that messages can be replied to.
        """
        pass

    def test_that_messages_can_be_deleted(self):
        """ Tests that messages can be deleted
        """
        pass

    @classmethod
    def tearDownClass(cls):
        super(MessageTestCase, cls).tearDownClass()
