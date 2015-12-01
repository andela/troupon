from django.shortcuts import render, redirect
from account.views import LoginRequiredMixin
from django.template import RequestContext, loader, Template, Engine
from django.views.generic.base import TemplateView
from userprofile.forms import UserProfileForm, TrouponMerchantForm
from userprofile.models import UserProfile
from deals.models import STATE_CHOICES
from django.contrib import messages
from django.http import HttpResponse

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

class MerchantView(TemplateView):

    template_name = "userprofile/merchant.html"

    def get(self, request, *args, **kwargs):
        context = {
                'show_subscribe': False,
                'show_search': False,
                'states': { 'choices': STATE_CHOICES,  'default': 25 },
            }
        #context['form']= TrouponMerchantForm()
        return self.render_to_response(context)

    def post(self, request, **kwargs):

        merchantform = TrouponMerchantForm(request.POST)

        if merchantform.errors:
            context = {
                'show_subscribe': False,
                'show_search': False,
                'states': { 'choices': STATE_CHOICES,  'default': 25 },
            }
            empty = "Please check that you have entered the correct form data"
            messages.add_message(request, messages.INFO,empty )
            return render(request, self.template_name, context)
        
        if merchantform.is_valid():
            merchantform.save()
            return HttpResponse("success", content_type="text/plain")








