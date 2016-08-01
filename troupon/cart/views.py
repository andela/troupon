import os

from carton.cart import Cart

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.generic import View

from authentication.views import LoginRequiredMixin
from deals.models import Deal
from .models import UserShippingDetails


class CheckoutView(LoginRequiredMixin, View):
    """
    Creates a checkout page.

    Attributes:
        template_name: name of the template that renders the view
        stripe_secret_api_key: the secret API key for our stripe account
        stripe_publishable_api_key: the publishable API key
    """

    template_name = 'cart/checkout.html'
    stripe_secret_api_key = os.getenv('STRIPE_SECRET_API_KEY')
    stripe_publishable_api_key = os.getenv('STRIPE_PUBLISHABLE_API_KEY')

    def get(self, request, **kwargs):
        """
        Create checkout page.

        Gets shopping information from cart and sends it to the payment app
        in form of a dict. It then renders the checkout template which can then
        be used to pay.

        Args:
            request: The incoming get request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A template rendered with the payment details context
        """
        cart = Cart(request.session)
        amount = cart.total
        amount_in_cents = int(amount) * 100
        title = "Total payment expected"
        description = "Troupon shopping"

        payment_details = {
            "title": title,
            "key": self.stripe_publishable_api_key,
            "amount": amount_in_cents,
            "description": description,
            "currency": "usd",
        }
        request.session['payment_details'] = payment_details

        context = {
            "amount": amount,
            "title": title,
            "description": description,
            "payment_details": payment_details,
        }
        return render(request, self.template_name, context)


class AddToCartView(LoginRequiredMixin, View):
    """
    Add items to cart.

    When a logged in person clicks on Add to cart on a deal, this view
    adds the item to the cart.

    Attributes:
        LoginRequiredMixin: Ensures the user is logged in
        View: Normal django view
    """

    def post(self, request, **kwargs):
        """
        Add item to cart.

        Args:
            request: The incoming post request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A redirect to the deals homepage
        """
        dealid = request.POST.get('dealid')

        deal = Deal.objects.get(id=dealid)

        cart = Cart(request.session)

        cart.add(deal, price=deal.price)

        return redirect('/')


class AddShippingDetails(LoginRequiredMixin, View):
    """
    Add shipping details of user.

    When a logged in user clicks on proceed to checkout this view
    gets the shipping details of the user

    Attributes:
        LoginRequiredMixin: Ensures the user is logged in
        View: Normal django view
    """

    def get(self, request):
        cart = Cart(request.session)
        context = {'cart': cart}
        return TemplateResponse(request, 'cart/shipping.html', context)

    def post(self, request, **kwargs):
        """
        Add shipping details.

        Args:
            request: The incoming post request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A redirect to the checkout page
        """
        street = request.POST.get('street')
        state = request.POST.get('state')
        telephone = request.POST.get('telephone')
        user = request.user.profile
        shipping = UserShippingDetails(user=user, street=street, state=state, telephone=telephone)
        shipping.save()
        return TemplateResponse(request, 'cart/checkout.html')


class ViewCartView(LoginRequiredMixin, View):
    """
    Allow user to view all the items in the cart.

    A logged in user with items in the cart can see a
    summary of them and their prices.

    Attributes:
        LoginRequiredMixin: Ensures the user is logged in
        View: Normal django view
    """

    def get(self, request, **kwargs):
        """
        Show cart items.

        Args:
            request: The incoming get request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A template rendered with all the cart items.
        """
        cart = Cart(request.session)

        context = {'cart': cart}
        return TemplateResponse(request, 'cart/cart.html', context)


class ClearCartView(LoginRequiredMixin, View):
    """
    Clear items in cart.

    When triggered, removes every item in the cart session
    and leaves it empty.

    Attributes:
        LoginRequiredMixin: Ensures the user is logged in
        View: Normal django view
    """

    def get(self, request, **kwargs):
        """
        Get cart from session and remove everything from it.

        Args:
            request: The incoming get request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A redirect to the deals homepage
        """
        cart = Cart(request.session)

        cart.clear()

        return redirect('/')


class RemoveItemView(LoginRequiredMixin, View):
    """
    Remove item from cart.

    When triggered, removes a particular item from the cart session
    based on its id.

    Attributes:
        LoginRequiredMixin: Ensures the user is logged in
        View: Normal django view
    """

    def post(self, request, **kwargs):
        """
        Remove item from cart.

        Args:
            request: The incoming get request object
            **kwargs: Any keyword arguments passed to the function

        Returns:
            A redirect to the deals homepage
        """
        dealid = request.POST.get('dealid')

        deal = Deal.objects.get(id=dealid)
        cart = Cart(request.session)
        cart.remove(deal)

        return redirect('/')
