"""Serializers for the merchant app."""
from deals.models import Deal
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date, timedelta


class UserSerializer():
    class Meta:
        model = User

        fields = ('id', 'username', 'password')


class DealSerializer(serializers.ModelSerializer):
    class Meta():
        model = Deal

        fields = ('id', 'title', 'slug', 'description', 'advertiser',
                  'original_price', 'price', 'category', 'currency',
                  'state', 'quorum', 'disclaimer', 'address',
                  'max_quantity_available', 'date_created', 'date_end',
                  'active', 'image')

        read_only_fields = ('id', 'slug', 'advertiser', 'date_created')
        write_only_fields = ('category', 'max_quantity_available', 'price',
                             'original_price')
