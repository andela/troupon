from django.shortcuts import render, redirect
from account.views import LoginRequiredMixin
from django.template import RequestContext, loader, Template, Engine
from django.views.generic.base import TemplateView
from userprofile.forms import UserProfileForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile, Merchant
from deals.models import STATE_CHOICES
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.views import login
from django_otp.forms import OTPTokenForm
from functools import partial
from nexmo import send_message
from .onetimepassword import CustomTOTPDevice
from nexmo.libpynexmo.nexmomessage import NexmoMessage
from django.conf import settings

# Create your views here.
class Userprofileview(LoginRequiredMixin, TemplateView):
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
        'states': { 'choices': STATE_CHOICES,  'default': 25 },
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
                'states': { 'choices': STATE_CHOICES,  'default': 25 },
            }
            empty = "form should not be submitted empty"
            messages.add_message(request, messages.INFO,empty )
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
                'states': { 'choices': STATE_CHOICES,  'default': 25 },
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

        merchant.save() ###check
        customTOTPDevice = CustomTOTPDevice()           
        token = customTOTPDevice.generate_token()
        msg = {
                'reqtype': 'json',
                'api_key':settings.NEXMO_USERNAME ,
                'api_secret': settings.NEXMO_PASSWORD,
                'from': settings.NEXMO_FROM,
                'to': telephone,
                'text': str(token),
            }
        sms = NexmoMessage(msg)
        response = sms.send_request()
        if response:
            print response
            return HttpResponse("success", content_type="text/plain")
        else:
            context = {
                'show_subscribe': False,
                'show_search': False,
                'states': { 'choices': STATE_CHOICES,  'default': 25 },
            }
        empty = "Please verify that you entered the correct information"
        messages.add_message(request, messages.ERROR,empty )
        return self.render_to_response(context)

class VerificationView(TemplateView, LoginRequiredMixin):

    template_name = 'userprofile/verify.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['authentication_form']=partial(OTPTokenForm, request.user)
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):

        token = request.POST.get('token')
        customTOTPDevice = CustomTOTPDevice()
        result = customTOTPDevice.verify_token(token)
        print result

        if result == True:
            return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("failure", content_type="text/plain")














