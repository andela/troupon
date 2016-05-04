"""Serializers for the payment app."""
from rest_framework import serializers

from models import Purchases


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction instances.
    """

    class Meta:
        model = Purchases
        fields = ('id', 'item', 'price', 'quantity', 'title',
                  'description', 'stripe_transaction_id',
                  'stripe_transaction_status')
