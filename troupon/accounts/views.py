import pyotp
from nexmo.libpynexmo.nexmomessage import NexmoMessage
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.conf import settings
from django.utils.text import slugify
from django.template.response import TemplateResponse

from authentication.views import LoginRequiredMixin
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from conversations.models import Message
from deals.models import COUNTRY_CHOICES, ALL_LOCATIONS, KENYAN_LOCATIONS, NIGERIAN_LOCATIONS, Advertiser
from merchant.models import Merchant
from payment.models import Purchases

secret_key = settings.OTP_SECRET_KEY
totp_token = pyotp.TOTP(secret_key, interval=180)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Handles display of the user profile details
    """
    def get(self, request):
        """Renders a page showing user details
        """
        profile = self.request.user.profile
        country = dict(COUNTRY_CHOICES).get(profile.country)
        location = dict(ALL_LOCATIONS).get(profile.location)
        context = {
            'user': self.request.user,
            'profile': profile,
            'country': country,
            'location': location,
            'profile.location': profile.location,
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'View Profile', },
            ]
        }

        return TemplateResponse(request, 'account/view_profile.html', context)


class EditProfileView(LoginRequiredMixin, TemplateView):
    """
    Handles display of the account profile form view
    """
    form_class = UserProfileForm
    template_name = "account/edit_profile.html"

    def get_context_data(self, **kwargs):
        context_var = super(EditProfileView, self).get_context_data(**kwargs)
        context_var.update({
            'profile': self.request.user.profile,
            'countries': {'choices': COUNTRY_CHOICES, 'default': 2},
            'locations_kenya': {'choices': KENYAN_LOCATIONS, 'default': 84},
            'locations_nigeria': {'choices': NIGERIAN_LOCATIONS, 'default': 25},
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Edit Profile', },
            ]
        })
        return context_var

    def post(self, request, **kwargs):

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        profile = UserProfile.objects.get(id=request.user.profile.id)
        form_dict = profile.check_diff(request.POST)

        form = self.form_class(
            form_dict, instance=request.user.profile)

        if form.errors:
            context_var = {}
            empty = "Form should not be submitted empty"
            messages.add_message(request, messages.INFO, empty)
            return TemplateResponse(request, 'account/edit_profile.html', context_var)

        if form.is_valid():
            form.save()

            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.add_message(
                request, messages.SUCCESS, 'Profile Updated!')
            return redirect(
                reverse('account_profile_edit'),
                context_instance=RequestContext(request)
            )


class TransactionsView(TemplateView):
    """View transactions for a user"""

    def get(self, request):
        """Renders a page with a table showing a deal,
        quantity bought, time of purchase, and its price
        """
        user = self.request.user
        transactions = Purchases.objects.filter(user=user)

        context = {
            'transactions': transactions,
        }

        return TemplateResponse(request, 'account/transaction.html', context)


class MerchantIndexView(LoginRequiredMixin, TemplateView):
    """
    Shows the template for the 'Become a Merchant' call-to-action view
    OR redirects to show the the status of the merchant's application
    OR show the approved message with a link to the merchant dashboard.
    """

    def get(self, request, *args, **kwargs):
        # use the merchant status fields to determine which
        # view to show or redirect to:
        try:
            if not request.user.profile.merchant.enabled:
                return redirect(reverse('account_merchant_verify'))
            else:
                return redirect(reverse('account_merchant_confirm'))

        except AttributeError:
            pass

        # define the base breadcrumbs for this view:
        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', },
                {'name': 'Get Started', },
            ]
        }
        template_name = 'account/become_a_merchant.html'
        return TemplateResponse(request, template_name, context)


class MerchantRegisterView(LoginRequiredMixin, TemplateView):

    template_name = "account/register_merchant.html"

    def get(self, request, **kwargs):

        # define the base breadcrumbs for this view:
        context = {
            'profile': self.request.user.profile,
            'countries': {'choices': COUNTRY_CHOICES, 'default': 2},
            'locations_kenya': {'choices': KENYAN_LOCATIONS, 'default': 84},
            'locations_nigeria': {'choices': NIGERIAN_LOCATIONS, 'default': 25},
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', 'url': reverse('account_merchant')},
                {'name': 'Merchant Register', },
            ]
        }

        if not self.request.user.profile.is_complete():
            mesg = """Please complete your profile information
             before applying to become a merchant."""
            messages.add_message(self.request, messages.INFO, mesg)
            return redirect(reverse('account_profile_edit'))

        return TemplateResponse(request, self.template_name, context)

    def post(self, request, **kwargs):

        name = request.POST.get('name')
        context = {
            'profile': self.request.user.profile,
            'countries': {'choices': COUNTRY_CHOICES, 'default': 2},
            'locations_kenya': {'choices': KENYAN_LOCATIONS, 'default': 84},
            'locations_nigeria': {'choices': NIGERIAN_LOCATIONS, 'default': 25},
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', 'url': reverse('account_merchant')},
                {'name': 'Merchant Register', },
            ]
        }

        try:
            advertiser = Advertiser.objects.get(name__exact=name)
            mssg = "Company Name Already taken/exists"
            messages.add_message(request, messages.ERROR, mssg)
            return TemplateResponse(request, self.template_name, context)

        except Advertiser.DoesNotExist:

            country = int(request.POST.get('user_country'))
            if country == 1:
                location = int(request.POST.get('nigeria_user_location'))
            elif country == 2:
                location = int(request.POST.get('kenya_user_location'))
            telephone = request.POST.get('telephone')
            intlnumber = request.POST.get('intlnumber')
            email = request.POST.get('email')
            address = request.POST.get('address')
            slug = slugify(name)
            userprofile = request.user.profile
            logo = request.FILES.get('logo')
            merchant = Merchant(
                name=name, country=country, location=location,
                telephone=telephone, email=email,
                address=address, slug=slug,
                intlnumber=intlnumber, logo=logo,
                userprofile=userprofile
            )

            merchant.save()
            token = totp_token.now()
            msg = {
                'reqtype': 'json',
                'api_key': settings.NEXMO_USERNAME,
                'api_secret': settings.NEXMO_PASSWORD,
                'from': settings.NEXMO_FROM,
                'to': intlnumber,
                'text': str(token),
            }
            sms = NexmoMessage(msg)
            response = sms.send_request()
            if response:
                return redirect(
                    reverse('account_merchant_verify'))


class MerchantVerifyView(LoginRequiredMixin, TemplateView):

    template_name = "account/verify_merchant.html"

    def get(self, request, *args, **kwargs):

        # define the base breadcrumbs for this view:
        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', 'url': reverse('account_merchant')},
                {'name': 'OTP Verification', },
            ]
        }

        try:
            if request.user.profile.merchant:
                return TemplateResponse(request, self.template_name, context)

        except AttributeError:
            return redirect(reverse('account_profile_edit'))

    def post(self, request, *args, **kwargs):

        token = request.POST.get('token')
        result = totp_token.verify(token)

        if result is True:

            merchant = Merchant.objects.get(
                userprofile_id=request.user.profile
            )
            merchant.enabled = True
            merchant.save()

            return redirect(reverse('account_merchant_confirm'))
        else:
            mssg = "OTP Verification Failed. Resend OTP "
            messages.add_message(request, messages.ERROR, mssg)
            return redirect(reverse('account_merchant_verify'))


class MerchantConfirmView(LoginRequiredMixin, TemplateView):
    template_name = "account/confirm_merchant.html"

    def get(self, request, *args, **kwargs):
        # define the base breadcrumbs for this view:
        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', 'url': reverse('account_merchant')},
                {'name': 'Confirm Merchant', },
            ]
        }

        try:
            if request.user.profile.merchant:

                if(not Message.confirmation_sent(request.user)):
                    # send message to admin that a merchant has been enabled
                    body = """%s %s just verified his phone number.
                    He is awaiting approval for his request to
                    become a merchant.""" % (
                        request.user.first_name,
                        request.user.last_name)

                    Message.send('Account', 'Merchant Approval',
                                            body, request.user)
                    mesg = """A message has been sent to the admin with your
                    application to become a merchant."""
                    messages.add_message(request, messages.INFO, mesg)

                return TemplateResponse(request, self.template_name, context)

        except AttributeError:
            return redirect(reverse('account_profile_edit'))


class MerchantResendOtpView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        try:
            if request.user.profile.merchant:
                merchant = get_object_or_404(
                    Merchant,
                    userprofile_id=request.user.profile
                )
            intlnumber = merchant.intlnumber
            token = totp_token.now()
            msg = {
                'reqtype': 'json',
                'api_key': settings.NEXMO_USERNAME,
                'api_secret': settings.NEXMO_PASSWORD,
                'from': settings.NEXMO_FROM,
                'to': intlnumber,
                'text': str(token),
            }
            sms = NexmoMessage(msg)
            response = sms.send_request()

            if response:
                mssg = "OTP Verification number has been sent."
                messages.add_message(request, messages.ERROR, mssg)
                return redirect(reverse('account_merchant_verify'))

        except AttributeError:
            return redirect(reverse('account_profile_edit'))


class UserChangePasswordView(LoginRequiredMixin, TemplateView):

    """
    Class defined to change user password.
    """

    template_name = "account/user_changepassword.html"

    def get(self, request, *args, **kwargs):
        # define the base breadcrumbs for this view:
        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Change Password', },
            ]
        }

        return TemplateResponse(request, self.template_name, context)

    def post(self, request, **kwargs):

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        current_password = request.POST.get('current_pasword', '')
        user = User.objects.get(id=request.user.id)

        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Change Password', },
            ]
        }
        if not user.check_password(current_password):
            context.update(csrf(request))
            mssg = "Your current password is incorrect"
            messages.add_message(request, messages.INFO, mssg)
            return TemplateResponse(request, self.template_name, context)

        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                mssg = "Password Successfully Changed!"
            else:
                context.update(csrf(request))
                mssg = "Password Mismatch"

            messages.add_message(request, messages.INFO, mssg)
            return TemplateResponse(request, self.template_name, context)

        if not password1 and not password2:
            context.update(csrf(request))
            mssg = "Passwords should match or field should not be left empty"
        else:
            context.update(csrf(request))
            mssg = "Passwords should match or field should not be left empty"

        messages.add_message(request, messages.INFO, mssg)
        return TemplateResponse(request, self.template_name, context)
