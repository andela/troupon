from conversations.models import Message
from django.test import TestCase
from django.contrib.auth.models import User


class MessageTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(MessageTestCase, cls).setUpClass()
        cls.user1 = User.objects.create_user(
            'user1', 'user1@example.com', '123456'
        )
        cls.user2 = User.objects.create_user(
            'user2', 'user2@example.com', '123456'
        )
        cls.msg_stub = {
            'sender': cls.user1,
            'recipient': cls.user2,
            'subject': 'Subject Text',
            'body': 'Body Text',
        }

    def test_that_messages_can_be_created(self):
        """Tests that messages can be created
        """
        message = Message(**self.msg_stub)
        message.save()
        self.assertIsNotNone(message.id)

    def test_that_messages_can_be_read(self):
        """Tests that messages can be read
        """
        message = Message(**self.msg_stub)
        message.save()
        self.assertIsNotNone(message.id)
        message = Message.objects.latest('sent_at')
        self.assertEqual(message.subject, self.msg_stub['subject'])

    def test_that_messages_can_be_replied_to(self):
        """Tests that messages can be replied to.
        """
        message = Message(**self.msg_stub)
        message.save()
        self.assertIsNotNone(message.id)
        self.msg_stub['parent_msg'] = message

        reply_msg = Message(**self.msg_stub)
        reply_msg.save()
        self.assertIsNotNone(reply_msg.id)
        self.assertEqual(reply_msg.parent_msg, self.msg_stub['parent_msg'])

    def test_that_messages_can_be_deleted(self):
        """Tests that messages can be deleted
        """
        message = Message(**self.msg_stub)
        message.save()
        self.assertIsNotNone(message.id)
        message.delete()
        self.assertIsNone(message.id)

    @classmethod
    def tearDownClass(cls):
        super(MessageTestCase, cls).tearDownClass()
