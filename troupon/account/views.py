from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect

from authentication.views import LoginRequiredMixin
from deals.models import STATE_CHOICES
from account.forms import UserProfileForm
from account.models import UserProfile


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Handles display of the account profile form view
    """
    form_class = UserProfileForm
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context_var = super(UserProfileView, self).get_context_data(**kwargs)
        context_var.update({
            'profile': self.request.user.profile,
            'states': {'choices': STATE_CHOICES, 'default': 25},
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Profile', },
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
            empty = "form should not be submitted empty"
            messages.add_message(request, messages.INFO, empty)
            return render(request, 'account/profile.html', context_var)

        if form.is_valid():
            form.save()

            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.add_message(
                request, messages.SUCCESS, 'Profile Updated!')
            return redirect(
                reverse('account_profile'),
                context_instance=RequestContext(request)
            )


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
            if not request.user.userprofile.merchant.enabled:
                redirect(reverse('account_mechant_verify'))
            else:
                redirect(reverse('account_merchant_confirm'))

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
        return render(request, template_name, context)


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

        return render(request, self.template_name, context)

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
            return render(request, self.template_name, context)

        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return HttpResponseRedirect('/')
            else:

                context.update(csrf(request))
                mssg = "Password Mismatch"
                messages.add_message(request, messages.INFO, mssg)
                return render(request, self.template_name, context)

        if not password1 and not password2:

            context.update(csrf(request))
            mssg = "Passwords should match or field should not be left empty"
            messages.add_message(request, messages.INFO, mssg)
            return render(request, self.template_name, context)

        if not password1 or not password2:

            context.update(csrf(request))
            mssg = "Passwords should match or field should not be left empty"
            messages.add_message(request, messages.INFO, mssg)

            return render(request, self.template_name, context)
