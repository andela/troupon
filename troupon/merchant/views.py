from datetime import date, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib import messages

from deals.models import Deal, Category, Advertiser, \
    COUNTRY_CHOICES, ALL_LOCATIONS, NIGERIAN_LOCATIONS, KENYAN_LOCATIONS, CURRENCY_CHOICES
from deals.baseviews import DealListBaseView
from merchant.forms import DealForm
from merchant.mixins import MerchantMixin
from merchant.models import Merchant
from payment.models import TransactionHistory, Purchases


class ManageDealsView(MerchantMixin, DealListBaseView):

    """Manage deals"""
    def get(self, request):
        """Renders a listing page for all deals that was created by a merchant
        """

        advertiser_id = request.user.profile.merchant.advertiser_ptr.id
        deals = Deal.objects.filter(advertiser=advertiser_id)

        list_title = "My Deals"
        list_description = "All deals posted by you"

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            queryset=deals,
            title=list_title,
            description=list_description,
            action_url='merchant_manage_deal',
            pagination_base_url=reverse('merchant_manage_deals')
        )
        context = {
            'rendered_deal_list': rendered_deal_list,
        }

        return render(request, 'merchant/deals.html', context)


class ManageDealView(MerchantMixin, View):
    """Manage a single deal"""
    def get(self, request, deal_slug):
        """Renders a page showing a deal that was created by a merchant
        """
        deal = get_object_or_404(Deal, slug=deal_slug)
        if deal.advertiser != request.user.profile.merchant.advertiser_ptr:
            messages.add_message(
                request, messages.ERROR,
                'You are not allowed to manage this deal'
            )
            return redirect(reverse('merchant_manage_deals'))
        context_data = {
            'deal': deal,
            'breadcrumbs': [
                {'name': 'Merchant', 'url': reverse('merchant_manage_deals')},
                {'name': 'Deals', }
            ]
        }
        return render(request, 'merchant/deal.html', context_data)

    def post(self, request, deal_slug):
        """Updates information about a deal that was created by a merchant.
        """
        dealform = DealForm(request.POST, request.FILES)
        deal = get_object_or_404(Deal, slug=deal_slug)
        if deal.advertiser != request.user.profile.merchant.advertiser_ptr:
            messages.add_message(
                request, messages.ERROR,
                'You are not allowed to manage this deal'
            )
            return redirect(reverse('merchant_manage_deals'))

        if dealform.is_valid():
            dealform.save(deal)
            messages.add_message(
                request, messages.SUCCESS, 'The deal was updated successfully.'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'An error occurred while performing the operation.'
            )
        return redirect(
            reverse('merchant_manage_deal', kwargs={'deal_slug': deal.slug})
        )


class TransactionsView(MerchantMixin, View):
    """View transactions for a merchant"""
    def get(self, request):
        """Renders a page with a table showing a deal, its buyer,
        quantity bought, time of purchase, and its price
        """
        user = self.request.user
        merchant = Merchant.objects.get(userprofile=user.pk)
        advertiser = Advertiser.objects.get(name=merchant.name)
        transactions = Purchases.objects.filter(advertiser=advertiser.id)

        context = {
            'transactions': transactions,
        }

        return render(request, 'merchant/transactions.html', context)


class TransactionView(MerchantMixin, View):
    """View transactions detail for a merchant"""
    def get(self, request, transaction_id):
        """Renders a detailed view about a transaction """
        context_data = []
        return render(request, 'merchant/transactions.html', context_data)


class CreateDealView(MerchantMixin, TemplateView):

    template_name = "merchant/deal_create.html"

    def get_context_data(self, **kwargs):
        context_var = super(CreateDealView, self).get_context_data(**kwargs)
        context_var.update({
            'countries': {'choices': COUNTRY_CHOICES, 'default': 2},
            'locations_kenya': {'choices': KENYAN_LOCATIONS, 'default': 84},
            'locations_nigeria': {'choices': NIGERIAN_LOCATIONS, 'default': 25},
            'currency': {'choices': CURRENCY_CHOICES, 'default': 1},
            'category': Category.objects.order_by('name')
        })
        return context_var

    def post(self, request, **kwargs):
        """Create a deal."""
        price = request.POST.get('price')
        original_price = request.POST.get('original_price')
        currency = request.POST.get('currency')
        country = int(request.POST.get('user_country'))

        if country == 1:
            location = int(request.POST.get('nigeria_user_location'))
        elif country == 2:
            location = int(request.POST.get('kenya_user_location'))

        quorum = request.POST.get('quorum') or 0
        disclaimer = request.POST.get('disclaimer')
        description = request.POST.get('description')
        title = request.POST.get('title')
        address = request.POST.get('address')
        max_quantity_available = request.POST.get('max_quantity_available')
        active = request.POST.get('active')
        active = True if active else False
        image = request.FILES.get('image')

        date_end_unicode = request.POST.get('date_end') or \
            (date.today() + timedelta(days=2)).isoformat()
        category_id = request.POST.get('category')
        advertiser_id = request.user.profile.merchant.advertiser_ptr.id

        category = Category.objects.get(id=category_id)
        advertiser = Advertiser.objects.get(id=advertiser_id)

        ymd = date_end_unicode.split('-')
        date_end = date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        today = date.today()

        duration = int(str(date_end - today).split(" ")[0])

        if date_end < today:
            messages.add_message(
                request, messages.ERROR,
                "You entered a date that's before today. Please try again"
            )
            return redirect(reverse('merchant_create_deal'))

        deal = Deal(
            price=price, original_price=original_price, currency=currency,
            country=country, location=location, category=category,
            quorum=quorum, disclaimer=disclaimer, description=description,
            address=address, max_quantity_available=max_quantity_available,
            date_end=date_end, active=active, image=image, title=title,
            advertiser=advertiser, duration=duration
        )

        deal.save()

        mssg = "Deal successfully created."
        messages.add_message(request, messages.ERROR, mssg)
        return redirect(reverse('merchant_manage_deals'))


class MerchantView(MerchantMixin, View):
    def get(self, request, merchant_slug):
        """Renders a view containing information about a merchant"""
        pass
