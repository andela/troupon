from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from hashs import UserHasher as Hasher
from forms import EmailForm
from emails import Mailgunner


class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)

    def post(self, request, *args, **kwargs):
        email_form = EmailForm(request.POST,auto_id=True)
        if email_form.is_valid():
            try:
                # get the account for that email if it exists:
                input_email = email_form.cleaned_data.get('email')
                registered_account = User.objects.get(email__exact=input_email)

                # generate a recovery hash url for that account:
                recovery_hash = Hasher.gen_hash(registered_account)
                recovery_hash_url = request.build_absolute_uri(reverse('account_reset_password', kwargs={'recovery_hash': recovery_hash}))
                
                # compose the email:
                recovery_email_context = RequestContext(request, {'recovery_hash_url': recovery_hash_url})
                recovery_email =  Mailgunner.compose(
                    sender = 'Troupon <support.troupon@andela.com>',
                    reciepient = registered_account.email,
                    subject = 'Troupon: Password Recovery',
                    html = loader.get_template('account/forgot_password_recovery_email.html').render(recovery_email_context),
                    text = loader.get_template('account/forgot_password_recovery_email.txt').render(recovery_email_context),
                )
                # send it and get the request status:
                email_status = Mailgunner.send(recovery_email)

                # inform the user of the status of the recovery mail:
                context = {
                    'page_title': 'Forgot Password',
                    'registered_account':  registered_account,
                    'recovery_mail_status': email_status,
                }
                return render(request, 'account/forgot_password_recovery_status.html', context)
            
            except ObjectDoesNotExist:
                # set a flash message:
                messages.add_message(request, messages.ERROR, 'The email you entered does not belong to a registered user!')

        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)


class ResetPasswordView(View):
    pass