"""Import statements."""
from django.shortcuts import render, redirect
from django.views.generic import View
import os
from django.template.response import TemplateResponse
from authentication.views import LoginRequiredMixin
from carton.cart import Cart
from deals.models import Deal


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
        """Update information."""
        cart = Cart(request.session)
        amount = cart.total
        amount_in_cents = int(amount) * 100
        title = "Total payment expected"
        description = "Troupon shopping"

        # store payment details in session
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
    """Adds item to cart.

    Returns:
        A redirect to the deals homepage
    """

    def post(self, request, **kwargs):
        """Save info in cart."""
        dealid = request.POST.get('dealid')

        deal = Deal.objects.get(id=dealid)

        cart = Cart(request.session)

        cart.add(deal, price=deal.price)

        return redirect('/')


class ViewCartView(LoginRequiredMixin, View):
    """Allow user to view all the items in the cart.

    Returns:
        A template rendered with all the cart items.
    """

    def get(self, request, **kwargs):
        """Show cart items."""
        cart = Cart(request.session)

        context = {'cart': cart}
        return TemplateResponse(request, 'cart/cart.html', context)


class ClearCartView(LoginRequiredMixin, View):
    """
    Clear items in cart.

    Returns:
        A redirect to the deals homepage
    """

    def get(self, request, **kwargs):
        """Get cart from session and remove everything from it."""
        # get the cart object from the session
        cart = Cart(request.session)

        # call the cart's clear method to remove everything from it
        cart.clear()

        # return a redirect to the deals homepage
        return redirect('/')


class RemoveItemView(LoginRequiredMixin, View):
    """
    Remove item from cart.

    Returns:
        A redirect to the deals homepage
    """

    def post(self, request, **kwargs):
        """Remove item from cart."""
        # get the deal slug from request
        dealid = request.POST.get('dealid')

        # query the deal using the unique slug
        deal = Deal.objects.get(id=dealid)

        # get the cart object from the session
        cart = Cart(request.session)

        # remove the queried deal object from the cart
        cart.remove(deal)

        # return a redirect to the deals homepage
        return redirect('/')
