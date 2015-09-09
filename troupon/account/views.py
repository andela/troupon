from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.context_processors import csrf

from hashs import UserHasher as Hasher
from forms import EmailForm, ResetPasswordForm
from emails import Mailgunner

import re


class UserSigninView(View):

    """User can signin to his/her account with email and password"""

    cls_default_msgs = {'signed_in': 'User is already signed in',
                        'not_signed_in': 'User is not signed in',
                        'invalid_param': 'Invalid signin parameters',
                        }

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            data = {'msg': {'content': self.cls_default_msgs['signed_in']}}

            # Replace this template before deployment to test or production
            t_stub = Template('{{msg.content}}')
            # Replace this template before deployment to test or production

            return HttpResponse(t_stub.render(Context(data)))
        else:
            data = {'msg': {'content': self.cls_default_msgs['not_signed_in']}}

            # Replace this template before deployment to test or production
            t_stub = Template('{{msg.content}}')
            # Replace this template before deployment to test or production

            return HttpResponse(t_stub.render(Context(data)))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            data = {'msg': {'content': self.cls_default_msgs['signed_in']}}

            # Replace this template before deployment to test or production
            t_stub = Template('{{msg.content}}')
            # Replace this template before deployment to test or production
            return HttpResponse(t_stub.render(Context(data)))
        else:
            email = self.request.POST.get('email', '')
            password = self.request.POST.get('password', '')
            user = authenticate(username=email, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                login(self.request, user)

                # Redirect to a success page.
                referer_view = self.get_referer_view(self.request)

                return HttpResponseRedirect(referer_view,
                                            'Redirect to /deals/ route')
            else:
                # Show an error page
                data = {'msg': {
                            'content': self.cls_default_msgs['invalid_param']
                            }
                        }
                t_stub = Template('{{msg.content}}')
                return HttpResponse(t_stub.render(Context(data)))

    def get_referer_view(self, request, default=None):
        '''
        Return the referer view of the current request
        Example:
            def some_view(request):
                ...
                referer_view = get_referer_view(request)
                return HttpResponseRedirect(referer_view, '/accounts/login/')
        '''
        # if the user typed the url directly in the browser's address bar
        referer = request.META.get('HTTP_REFERER')
        if not referer:
            return default

        # remove the protocol and split the url at the slashes
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        if referer[0] != request.META.get('SERVER_NAME'):
            return default

        # add the slash at the relative path's view and finished
        referer = u'/' + u'/'.join(referer[1:])
        return referer


class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        context.update(csrf(request))
        return render(request, 'account/forgot_password.html', context)

    def post(self, request, *args, **kwargs):
        email_form = EmailForm(request.POST,auto_id=True)
        if email_form.is_valid():
            try:
                # get the account for that email if it exists:
                input_email = email_form.cleaned_data.get('email')
                registered_user = User.objects.get(email__exact=input_email)

                # generate a recovery hash url for that account:
                recovery_hash = Hasher.gen_hash(registered_user)
                recovery_hash_url = request.build_absolute_uri(reverse('account_reset_password', kwargs={'recovery_hash': recovery_hash}))
                
                # compose the email:
                recovery_email_context = RequestContext(request, {'recovery_hash_url': recovery_hash_url})
                recovery_email =  Mailgunner.compose(
                    sender = 'Troupon <troupon@andela.com>',
                    reciepient = registered_user.email,
                    subject = 'Troupon: Password Recovery',
                    html = loader.get_template('account/forgot_password_recovery_email.html').render(recovery_email_context),
                    text = loader.get_template('account/forgot_password_recovery_email.txt').render(recovery_email_context),
                )
                # send it and get the request status:
                email_status = Mailgunner.send(recovery_email)

                # inform the user of the status of the recovery mail:
                context = {
                    'page_title': 'Forgot Password',
                    'registered_user':  registered_user,
                    'recovery_mail_status': email_status,
                }
                return render(request, 'account/forgot_password_recovery_status.html', context)
            
            except ObjectDoesNotExist:
                # set an error message:
                messages.add_message(request, messages.ERROR, 'The email you entered does not belong to a registered user!')

        context = {
            'page_title': 'Forgot Password',
            'email_form': email_form, 
        }
        context.update(csrf(request))
        return render(request, 'account/forgot_password.html', context)


class ResetPasswordView(View):
    
    def get(self, request, *args, **kwargs):
        # get the recovery_hash captured in url
        recovery_hash = kwargs['recovery_hash']
        
        # reverse the hash to get the user (auto-authentication)
        user = Hasher.reverse_hash(recovery_hash)

        if user is not None:
            if user.is_active:
                # save the user in session:
                request.session['recovery_user_pk'] = user.pk

                # render the reset password view template.
                context = {
                    'page_title': 'Reset Password',
                    'reset_password_form': ResetPasswordForm(auto_id=True),
                }
                context.update(csrf(request))
                return render(request, 'account/reset_password.html', context)
            else:
                # set an 'account not activated' error message and return forbidden response:
                messages.add_message(request, messages.ERROR, 'Account not activated!')
                return HttpResponse(
                    'Account not activated!',
                    status_code = 403,
                    reason_phrase = 'You are not allowed to view this content because your account is not activated!'
                )
        else:
            # raise 404 when the hash doesn't return a user:
            raise Http404("/User does not exist")

    def post(self, request, *args, **kwargs):
        reset_password_form = ResetPasswordForm(request.POST,auto_id=True)
        if reset_password_form.is_valid():
            try:
                # get the recovery_user from the session:
                recovery_user_pk = request.session['recovery_user_pk'] 
                user = User.objects.get(pk=recovery_user_pk)

                # change the user's password to the new password:
                new_password = reset_password_form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()

                # inform the user thru a flash message:
                messages.add_message(request, messages.INFO, 'Your password was changed successfully!')

                # redirect the user to the sign in:
                return redirect(reverse('signin'))
            
            except ObjectDoesNotExist:
                # set an error message:
                messages.add_message(request, messages.ERROR, 'You are not allowed to perform this action!')
                return HttpResponse( 'Action not allowed!', status_code = 403 )

        context = {
            'page_title': 'Forgot Password',
            'email_form': reset_password_form, 
        }
        context.update(csrf(request))
        return render(request, 'account/forgot_password.html', context)