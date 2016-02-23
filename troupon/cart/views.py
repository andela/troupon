from django.shortcuts import render
from django.views.generic import View
import os
from authentication.views import LoginRequiredMixin


class CheckoutView(LoginRequiredMixin, View):
    """
    Creates a checkout page

    Attributes:
        template_name: name of the template that renders the view
        stripe_secret_api_key: the secret API key for our stripe account
        stripe_publishable_api_key: the publishable API key
    """
    template_name = 'cart/checkout.html'
    stripe_secret_api_key = os.getenv('STRIPE_SECRET_API_KEY')
    stripe_publishable_api_key = os.getenv('STRIPE_PUBLISHABLE_API_KEY')

    def get(self, request, *args, **kwargs):
        """
        creates a dummy checkout page

        Sets up a dummy page that users can pay for goods worth $23

        Args:
            request: the request object calling the view

        Return:
            a page that displays a stripe button for making payment
            of $23
        """
        amount = 23
        amount_in_cents = amount * 100
        payment_details = {
            "key": self.stripe_publishable_api_key,
            "description": "Hairless Armpits",
        }

        context = {
            "amount": amount,
            "amount_in_cents": amount_in_cents,
            "payment_details": payment_details,
        }

        # store payment details in session
        payment_details = {
            "amount": amount_in_cents,
            "description": "Hairless Armpits",
            "currency": "usd",
        }
        request.session['payment_details'] = payment_details

        return render(request, self.template_name, context)
