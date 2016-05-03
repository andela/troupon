"""Generic API configuration."""
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions

from deals.models import Advertiser
from payment.models import Purchases
from payment.serializers import TransactionSerializer


class TransationsList(generics.ListAPIView):
    """ A merchant can see a list of all transactions that contained
    items he/she is advertising on the site.
    """

    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advertiser_id = self.request.user.profile.merchant.advertiser_ptr.id
        advertiser = get_object_or_404(Advertiser, pk=advertiser_id)
        return Purchases.objects.filter(advertiser=advertiser)


class TransactionsDetails(generics.ListAPIView, generics.DestroyAPIView):
    """Using a transaction ID, a merchant can see the details of a particular transaction.
    """

    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        purchase_id = self.kwargs.get('pk')
        advertiser_id = self.request.user.profile.merchant.advertiser_ptr.id
        advertiser = get_object_or_404(Advertiser, pk=advertiser_id)
        return Purchases.objects.filter(advertiser=advertiser, id=purchase_id)
