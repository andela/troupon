from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Account
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from forms import EmailForm
# from email import send_email
from hashs import UserHashUtils as Hasher


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
                registered_account = Account.objects.get(email__exact=input_email)

                # generate a recovery hash url for that account:
                recovery_hash_base_url = "/account/recovery/"
                recovery_hash = Hasher.gen_hash(registered_account)
                recovery_hash_url =  recovery_hash_base_url + recovery_hash

                # compose the email:
                template = 'account/forgot_password_recovery_email'
                sender = 'Troupon <troupon@andela.com>'
                reciepient = registered_account.email
                subject = 'Troupon: Account Password Recovery'
                email_context = RequestContext(request, {
                    'registered_account':  registered_account,
                    'recovery_hash_url': recovery_hash_url,
                })
                html = loader.get_template('account/forgot_password_recovery_email.html').render(email_context)
                text = loader.get_template('account/forgot_password_recovery_email.txt').render(email_context)

                # send it and get request status:
                email_status = 200  # send_email(sender,reciepient, subject, text, html)

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


