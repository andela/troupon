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

    def post(self, request, **kwargs):
        """Update imformation.
        """
        amount = request.POST.get('price', 23)
        title = request.POST.get('title')
        description = request.POST.get('description') or "No description"
        amount_in_cents = amount * 100

        # store payment details in session
        payment_details = {
            "title": title,
            "key": self.stripe_publishable_api_key,
            "amount": amount_in_cents,
            "description": description,
            "currency": "usd",
        }

        context = {
            "amount": amount,
            "title": title,
            "description": description,
            "amount_in_cents": amount_in_cents,
            "payment_details": payment_details,
        }

        request.session['payment_details'] = payment_details

        return render(request, self.template_name, context)

