from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as UserAccount
from django.contrib import messages

from forms import EmailForm
from email import send_email
from hashs import gen_user_hash



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
                # get the account for that mail if it exists:
                input_email = email_form.cleaned_data.get('email')
                registered_account = UserAccount.objects.get(email__exact=input_email)

                # generate a recovery hash url for that account:
                recovery_hash_base_url = "/account/"
                recovery_hash_url = self.gen_user_hash(registered_account, recovery_hash_base_url)

                # compose the email:
                template = 'forgot_password_recovery_email'
                sender = 'Troupon <troupon@andela.com>'
                reciepient = registered_account.email
                subject = 'Troupon: Account Password Recovery'
                html =  render_template(template + '.html', {"recovery_hash_link": recovery_hash_link})
                text =  render_template(template + '.txt', {"recovery_hash_link": recovery_hash_link})

                # send it and get request status:
                email_status = send_email(sender,reciepient, subject, text, html)

                # inform the user of the status of the recovery mail:
                context = {
                    'page_title': 'Forgot Password',
                    'registered_account':  registered_account
                    'recovery_mail_status': email_status
                }
                return render(request, 'account/forgot_password_recovery_status.html', context)
            
            except DoesNotExist:
                # set a flash message:
                messages.add_message(request, messages.ERROR, 'The email you entered does not belong to a registered user!')

        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)


