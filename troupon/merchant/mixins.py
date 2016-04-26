from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class MerchantMixin(object):
    """
    Requires that the logged user is an approved merchant
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_approved_merchant():
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            if not request.user:
                return redirect(settings.LOGIN_URL)
            else:
                return redirect(reverse('account_merchant_register'))
        return super(MerchantMixin, self).dispatch(request, *args, **kwargs)
