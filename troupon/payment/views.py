import os
import stripe
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages


# Create your views here.
class PaymentProcessView(View):
    """
    Processes payments sent from stripe checkout.js
    """
    stripe_secret_api_key = os.getenv('STRIPE_SECRET_API_KEY')
    stripe_publishable_api_key = os.getenv('STRIPE_PUBLISHABLE_API_KEY')

    def post(self, request, *args, **kwargs):
        """process payment"""

        # Set your secret key:
        stripe.api_key = self.stripe_secret_api_key

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Get payment details from session
        payment_details = request.session.get('payment_details', None)

        # process payment if the payment details exist
        if payment_details:
            # Create the charge on Stripe's servers, charge the user's card
            try:
                charge = stripe.Charge.create(
                             # amount in cents, again
                             amount=payment_details['amount'],
                             currency=payment_details['currency'],
                             source=token,
                             description=payment_details['description']
                         )
                print charge.id
                print charge.created
            except stripe.error.CardError, e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except stripe.error.RateLimitError, e:
                # Too many requests made to the API too quickly
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except stripe.error.InvalidRequestError, e:
                # Invalid parameters were supplied to Stripe's API
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except stripe.error.AuthenticationError, e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except stripe.error.APIConnectionError, e:
                # Network communication with Stripe failed
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except stripe.error.StripeError, e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')
            except Exception, e:
                # Something else happened, completely unrelated to Stripe
                body = e.json_body
                err = body['error']

                message = '''
                Error!!! %s: %s\n%s
                ''' % (e.http_status, err['code'], err['message'])
                messages.add_message(request, messages.WARNING, message)

                url = reverse('payment_status')
                return HttpResponseRedirect(url + '?status=error')

            # return a success message if no errors are raised
            message = "Success!!! you payment has been received"
            messages.add_message(request, messages.WARNING, message)

            # delete payment details from session
            del request.session['payment_details']
            url = reverse('payment_status')
            return HttpResponseRedirect(url + '?status=complete')
        else:
            # return an error message as payment details are not in session
            message = "Error cannot get payment details"
            messages.add_message(request, messages.WARNING, message)
            url = reverse('payment_status')
            return HttpResponseRedirect(url + '?status=error')


class PaymentStatusView(View):
    """
    Display status of the transaction
    """
    template_name = 'payment/confirmation.html'

    def get(self, request, *args, **kwargs):
        # get status from querystring
        status = request.GET['status']
        return render(request, self.template_name, {'status': status})
