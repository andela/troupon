from django.db import models
from django.conf import settings


MESG_CHOICES = [
    (1, 'Account'),
    (2, 'Billing'),
    (3, 'General Info & Getting Started'),
    (4, 'Marketplace'),
]


class Message(models.Model):
    """A model representation of messages exchanged between
    the Administrator and merchant
    """
    subject = models.CharField(max_length=256)
    body = models.TextField()
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        null=True, blank=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recipient',
        null=True, blank=True)
    parent_msg = models.ForeignKey(
        'self',
        related_name='parent_rel',
        null=True,
        blank=True,
    )
    type = models.SmallIntegerField(choices=MESG_CHOICES, default=1)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)

    def is_unread(self):
        return self.read_at is None

    @property
    def count(self):
        return Message.objects.filter(parent_msg=self.id).count() + 1
