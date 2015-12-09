import pyotp
from nexmo.libpynexmo.nexmomessage import NexmoMessage
import time

from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse

from account.views import LoginRequiredMixin
from deals.models import STATE_CHOICES
from userprofile.forms import UserProfileForm
from userprofile.models import UserProfile, Merchant

secret_key = settings.OTP_SECRET_KEY
totp_token = pyotp.TOTP(secret_key, interval=180)

class Userprofileview(TemplateView, LoginRequiredMixin):

    """class that handles display of the homepage"""
    form_class = UserProfileForm
    template_name = "userprofile/profile.html"

    def get_context_data(self, **kwargs):
        context_var = super(Userprofileview, self).get_context_data(**kwargs)
        username = kwargs['username']
        if self.request.user.username == username:
            user = self.request.user
        else:
            pass

        context_var = {
        'show_subscribe': False,
        'show_search': False,
        'states': {'choices': STATE_CHOICES,'default': 25},
                    'profile': user.profile
                    }
        return context_var

    def post(self, request, **kwargs):

        form = self.form_class(
            request.POST, instance=request.user.profile)

        if form.errors:
            context_var = {
                'show_subscribe': False,
                'show_search': False,
                'states': {'choices': STATE_CHOICES, 'default': 25}
            }

            empty = "form should not be submitted empty"
            messages.add_message(request, messages.INFO, empty)
            return render(request, 'userprofile/profile.html', context_var)

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Profile Updated!')
            return redirect(
                '/userprofile/' + kwargs['username'],
                context_instance=RequestContext(request)
        )


class MerchantView(TemplateView, LoginRequiredMixin):

    template_name = "userprofile/merchant.html"

    def get(self, request, *args, **kwargs):
        context = {
                'show_subscribe': False,
                'show_search': False,
                'states': {'choices': STATE_CHOICES,'default': 25},
                }
        return self.render_to_response(context)

    def post(self, request, **kwargs):

        name = request.POST.get('name')
        state = request.POST.get('user_state')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        slug = request.POST.get('slug')
        userprofile = UserProfile.objects.get(id=request.user.id)

        merchant = Merchant(name=name, state=state, telephone=telephone, email=email, address=address, slug=slug, userprofile = userprofile )

        merchant.save()
        token = totp_token.now()
        msg = {
                'reqtype': 'json',
                'api_key':settings.NEXMO_USERNAME,
                'api_secret': settings.NEXMO_PASSWORD,
                'from': settings.NEXMO_FROM,
                'to': telephone,
                'text': str(token),
        }
        sms = NexmoMessage(msg)
        response = sms.send_request()
        print response
        #['messages'][0]['status'] == 0
        if response:
            return HttpResponse("success", content_type="text/plain")
        else:
            context = {
                'show_subscribe': False,
                'show_search': False,
                'states': {'choices': STATE_CHOICES, 'default': 25},
            }
        empty = "Phone number should start with country code."
        messages.add_message(request, messages.ERROR, empty)
        return self.render_to_response(context)


class VerificationView(TemplateView, LoginRequiredMixin):

    template_name = 'userprofile/verify.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        token = request.POST.get('token')
        result = totp_token.verify(token)

        if result == True:
            return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("failure", content_type="text/plain")
