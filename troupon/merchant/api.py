"""Generic API configuration."""
from datetime import date, timedelta

from django.shortcuts import get_object_or_404

from merchant.models import Merchant
from deals.models import Deal, Advertiser, Category, STATE_CHOICES
from merchant.serializers import DealSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response


class DealListAPIView(generics.ListCreateAPIView):
    """Authenticated merchant  can see a list of all his deals and create a deal."""
    serializer_class = DealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        current_merchant = get_object_or_404(Merchant, userprofile=user.pk)
        current_advertiser = get_object_or_404(Advertiser,
                                               name=current_merchant.name)
        deals = Deal.objects.filter(advertiser=current_advertiser)
        return deals

    def perform_create(self, serializer):
        date_end_unicode = self.request.POST.get('date_end') or \
            (date.today() + timedelta(days=2)).isoformat()
        category_id = self.request.POST.get('category')
        advertiser_id = self.request.user.profile.merchant.advertiser_ptr.id
        category = Category.objects.get(id=category_id)
        advertiser = Advertiser.objects.get(id=advertiser_id)

        ymd = date_end_unicode.split('-')
        date_end = date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        today = date.today()
        duration = int(str(date_end - today).split(" ")[0])

        serializer.save(duration=duration, advertiser=advertiser)


class DealActionsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Authenticated merchant can see a deal's details, update or delete it."""
    serializer_class = DealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        current_merchant = get_object_or_404(Merchant, userprofile=user.pk)
        current_advertiser = get_object_or_404(Advertiser,
                                               name=current_merchant.name)
        deal_pk = self.kwargs.get('pk')
        deal = Deal.objects.filter(advertiser=current_advertiser, pk=deal_pk)
        return deal
