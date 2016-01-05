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
