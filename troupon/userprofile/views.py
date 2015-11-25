from django.shortcuts import render, redirect
from account.views import LoginRequiredMixin
from django.views.generic.base import TemplateView
from userprofile.forms import UserProfileForm
from userprofile.models import UserProfile
from deals.models import STATE_CHOICES
from django.contrib import messages

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
            return render(request, 'account/profile.html', context_var)


        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Profile Updated!')
            return redirect(
                '/account/profile/user/' + kwargs['username'],
                context_instance=RequestContext(request)
            )
