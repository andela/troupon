from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Model

from authentication.views import LoginRequiredMixin
from forms import UserProfileForm


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
        })
        return context_var

    def post(self, request, **kwargs):

        form = self.form_class(
            request.POST, instance=request.user.profile)

        if form.errors:
            context_var = {}
            empty = "form should not be submitted empty"
            messages.add_message(request, messages.INFO, empty)
            return render(request, 'account/profile.html', context_var)

        if form.is_valid():
            form.save()
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

        # define the base breadcrumbs for this view:
        context = {
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Merchant', },
            ]
        }
        # use the merchant status fields to determine which
        # view to show or redirect to:
        try:
            if not request.user.userprofile.merchant.enabled:
                redirect(reverse('account_mechant_verify'))
            else:
                redirect(reverse('account_merchant_confirm'))

        except Model.DoesNotExist:
            template_name = 'account/become_a_merchant.html'
            context['breadcrumbs'].push({'name': 'Get Started', })

        return render(request, template_name, context)
