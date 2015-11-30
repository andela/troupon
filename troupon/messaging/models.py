from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """A model representation of messages exchanged between
    the Administrator and merchant
    """
    subject = models.CharField(max_length=256)
    body = models.TextField()
    sender = models.OneToOneField(
        User, related_name='sender', null=True, blank=True)
    recipient = models.ForeignKey(
        User, related_name='recipient', null=True, blank=True)
    parent_msg = models.ForeignKey(
        'self',
        related_name='parent_rel',
        null=True,
        blank=True,
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
