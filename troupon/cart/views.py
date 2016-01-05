from django.shortcuts import render
from django.views.generic import View
import os
from authentication.views import LoginRequiredMixin


class CheckoutView(LoginRequiredMixin, View):
    """
    Creates a checkout page
    """
    template_name = 'cart/checkout.html'
    stripe_secret_api_key = os.getenv('STRIPE_SECRET_API_KEY')
    stripe_publishable_api_key = os.getenv('STRIPE_PUBLISHABLE_API_KEY')

    def get(self, request, *args, **kwargs):
        """create a dummy checkout page"""
        amount_in_dollars = 23
        amount_in_cents = amount_in_dollars * 100

        payment_details = {
            "amount_in_dollars": amount_in_dollars,
            "amount_in_cents": amount_in_cents,
            "description": "Hairless Armpits",
            "currency": "usd",
            "key": self.stripe_publishable_api_key,
            "description": "Hairless Armpits",
        }

        context = {
            "payment_details": payment_details,
        }

        # store payment details in session
        request.session['payment_details'] = payment_details

        return render(request, self.template_name, context)
