from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class ManageDealsView(View):
    """Manage deals"""
    def get(self, request):
        """Renders a listing page for all deals that was created by a merchant
        """
        pass


class ManageDealView(View):
    """Manage a single deal"""
    def get(self, request, slug):
        """Renders a page showing a deal that was created by a merchant
        """
        pass

    def post(self, request, slug):
        """Updates information about a deal that was created by a merchant
        """
        pass


class TransactionsView(View):
    """View transactions for a merchant"""
    def get(self, request):
        """Renders a page with a table showing a deal, its buyer,
        quantity bought, time of purchase, and its price
        """
        pass


class TransactionView(View):
    """View transactions detail for a merchant"""
    def get(self, request, transaction_id):
        """Renders a detailed view about a transaction """
        pass


class CreateDealView(View):
    def get(self, request):
        """Renders a form for creating deals """
        pass

    def post(self, request):
        """Creates a deal"""
        pass


class MerchantView(View):
    def get(self, request, merchant_slug):
        """Renders a view containing information about a merchant"""
        pass
