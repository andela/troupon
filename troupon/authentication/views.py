import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email, ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.template import RequestContext, loader, Engine
from django.utils.decorators import method_decorator

from forms import UserSignupForm
from hashs import UserHasher as Hasher
from forms import EmailForm, ResetPasswordForm
from emails import SendGrid


class LoginRequiredMixin(object):
    """
    This class acts as a mixin to enforce user authentication.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method of the view class.

        Args: request, other arguments and key-value pairs.
        Returns: The call to the dispatch method of the parent class i.e
                 the View class
        """

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class UserLoginView(View):
    """
    This class allows a user to login to his/her account.

    Attributes:
        engine: the static reference of the template engine.
        cls_default_msgs: a dictionary of messages representing the current
                          user status.
    """
    engine = Engine.get_default()  # get static reference to template engine
    cls_default_msgs = {
        'not_signed_in': 'User is not signed in',
        'invalid_param': 'Invalid signin parameters. \
                        Possible causes might be: an incorrect username,\
                        an incorrect password or inexistent user account',
    }  # class default messages

    def get(self, *args, **kwargs):
        """Handles the get request to the 'login' named route.

        Returns: A HttpResponse with an authentication login template
        """
        if self.request.user.is_authenticated():
            # Obtain referring view
            referer_view = self.get_referer_view(self.request)
            return HttpResponseRedirect(referer_view)
        else:
            data = {'msg': {'content': self.cls_default_msgs['not_signed_in']}}
            # Replace template object compiled from template code
            # with an application template before push to production.
            # Use self.engine.get_template(template_name)
            template = self.engine.get_template('authentication/login.html')
            # Set result in RequestContext
            context = RequestContext(self.request, data)
            return HttpResponse(template.render(context))

    def post(self, *args, **kwargs):
        """Handles the POST request to the 'login' named route.

        Expects that an email/username and password is contained in
        the submitted form.

        Returns: A HttpResponse with a redirect if user is active,
                otherwise returns an authentication login template.
        """

        if self.request.user.is_authenticated():
            data = {'msg': {'content': self.cls_default_msgs['signed_in']}}
            # Replace template object compiled from template code
            # with an application template before push to production.
            # Use self.engine.get_template(template_name)
            template = self.engine.from_string('{{msg.content}}')
            # Set result in RequestContext
            context = RequestContext(self.request, data)
            return HttpResponse(template.render(context))
        else:
            username = self.request.POST.get('username', '')
            password = self.request.POST.get('password', '')
            csrfmiddlewaretoken = self.request.POST.get(
                'csrfmiddlewaretoken', '')
            # import pdb; pdb.set_trace()
            try:
                validate_email(username)
                user = User.objects.get(email__exact=username)
                username = user.username
            except (ValidationError, User.DoesNotExist) as e:
                # failing silently
                pass
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                login(self.request, user)

                # Redirect to a success page.
                referer_view = self.get_referer_view(self.request)

                return redirect('/')
            else:
                # Set error context
                error_msg = self.cls_default_msgs['invalid_param']
                messages.add_message(self.request, messages.INFO, error_msg)

                # Set template
                template = self.engine.get_template(
                    'authentication/login.html')

                # Set result in RequestContext
                context = RequestContext(self.request)
                return HttpResponse(template.render(context))

    def get_referer_view(self, request, default='/'):
        '''
        Returns the referer view of the current request
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


class UserLogoutView(View):
    """
    This class logs out an authenticated user from session.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('homepage'),
            'Redirect to home page')


class ForgotPasswordView(View):
    """
    This class allows user to send account recovery email.
    """

    def get(self, request, *args, **kwargs):
        """Handles GET requests to the 'account_forgot_password' named route.

        Returns: A forgot-password template rendered to a HttpResponse.
        """
        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        context.update(csrf(request))
        return render(request, 'authentication/forgot_password.html', context)

    def post(self, request, *args, **kwargs):
        """Handles the POST request to the 'account_forgot_password' named route.

        Args: request.
        Returns: A HttpResponse with a forgot_password_recovery_status template
                 otherwise, return forgot_password template.
        """
        email_form = EmailForm(request.POST, auto_id=True)
        if email_form.is_valid():
            try:
                # get the account for that email if it exists:
                input_email = email_form.cleaned_data.get('email')
                registered_user = User.objects.get(email__exact=input_email)

                # generate a recovery hash url for that account:
                recovery_hash = Hasher.gen_hash(registered_user)
                recovery_hash_url = request.build_absolute_uri(
                    reverse(
                        'account_reset_password',
                        kwargs={'recovery_hash': recovery_hash}
                    ))

                # compose the email:
                recovery_email_context = RequestContext(
                    request,
                    {'recovery_hash_url': recovery_hash_url})
                recovery_email = SendGrid.compose(
                    sender='Troupon <troupon@andela.com>',
                    recipient=registered_user.email,
                    subject='Troupon: Password Recovery',
                    html=loader.get_template(
                        'authentication/forgot_password_recovery_email.html'
                    ).render(recovery_email_context),
                    text=loader.get_template(
                        'authentication/forgot_password_recovery_email.txt'
                    ).render(recovery_email_context),
                )
                # send it and get the request status:
                email_status = SendGrid.send(recovery_email)

                # inform the user of the status of the recovery mail:
                context = {
                    'page_title': 'Forgot Password',
                    'registered_user': registered_user,
                    'recovery_mail_status': email_status,
                }
                return render(
                    request,
                    'authentication/forgot_password_recovery_status.html',
                    context)

            except ObjectDoesNotExist:
                # set an error message:
                messages.add_message(
                    request, messages.ERROR,
                    'The email you entered does not \
                    belong to a registered user!')

        context = {
            'page_title': 'Forgot Password',
            'email_form': email_form,
        }
        context.update(csrf(request))
        return render(request, 'authentication/forgot_password.html', context)


class ResetPasswordView(View):
    """This class allows user to reset password from recovery email.
    """

    def get(self, request, *args, **kwargs):
        """Handles GET requests to 'account_reset_password' named route.

        Resets user password.

        Returns:
            HttpResponse with reset_password template if user is active
            otherwise, flashes 'Account not activated' error to the session.
        """
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
                return render(
                    request,
                    'authentication/reset_password.html',
                    context
                )
            else:
                # set an 'account not activated' error message
                # and return forbidden response:
                messages.add_message(
                    request, messages.ERROR,
                    'Account not activated!')
                return HttpResponse(
                    'Account not activated!',
                    status_code=403,
                    reason_phrase='You are not allowed to view this content \
                    because your account is not activated!'
                )
        else:
            # raise 404 when the hash doesn't return a user:
            raise Http404("/User does not exist")

    def post(self, request, *args, **kwargs):
        """Handles POST requests to 'account_reset_password' named route.

        Returns: A HttpResponse with the reset_password template.
        """
        reset_password_form = ResetPasswordForm(request.POST, auto_id=True)
        if reset_password_form.is_valid():
            try:
                # get the recovery_user from the session:
                recovery_user_pk = request.session['recovery_user_pk']
                user = User.objects.get(pk=recovery_user_pk)

                # change the user's password to the new password:
                new_password = reset_password_form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()

                # inform the user through a flash message:
                messages.add_message(
                    request, messages.INFO,
                    'Your password was changed successfully!')

                # redirect the user to the sign in:
                return redirect(reverse('signin'))

            except ObjectDoesNotExist:
                # set an error message:
                messages.add_message(
                    request, messages.ERROR,
                    'You are not allowed to perform this action!')
                return HttpResponse('Action not allowed!', status_code=403)

        context = {
            'page_title': 'Reset Password',
            'reset_password_form': reset_password_form,
        }
        context.update(csrf(request))
        return render(request, 'authentication/reset_password.html', context)


class UserRegistrationView(View):
    """
    This class handles user signup.

    Attributes: template_name
    """
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to the 'register' named route.
        Returns: A HttpResponse with register template.
        """
        args = {}
        args.update(csrf(request))
        return render(request, 'authentication/register.html', args)

    def post(self, request):
        """Handles POST requests to 'register' named route.

        Raw data posted from form is received here,bound to form
        as dictionary and sent to unrendered django form for validation.

        Returns:
            A HttpResponse with a register template, otherwise, redirects to the
            login page.
        """
        usersignupform = UserSignupForm(request.POST)
        # get the user email address
        email = request.POST.get('email')
        signup_new_user = User.objects.filter(email__exact=email)
        if signup_new_user:
            args = {}
            args.update(csrf(request))
            mssg = "Email already taken please signup with another email"
            messages.add_message(request, messages.INFO, mssg)
            return render(request, 'authentication/register.html', args)

        if usersignupform.is_valid():
            usersignupform.save()
            new_user = User.objects.get(email__exact=email)

            # generate an activation hash url for new user account
            activation_hash = Hasher.gen_hash(new_user)
            activation_hash_url = request.build_absolute_uri(
                reverse(
                    'activate_account',
                    kwargs={'activation_hash': activation_hash},
                )
            )
            # compose the email
            activation_email_context = RequestContext(
                request,
                {'activation_hash_url': activation_hash_url,
                 'username': new_user.username,
                },

            )
            activation_email = SendGrid.compose(
                sender='Troupon <Noreplytroupon@andela.com>',
                recipient=new_user.email,
                subject='Troupon: ACTIVATE ACCOUNT',
                html=loader.get_template(
                    'authentication/activate_account_email.html'
                ).render(activation_email_context),
                text=loader.get_template(
                     'authentication/activate_account_email.txt'
                 ).render(activation_email_context),
            )
            # send mail to new_user
            activation_status = SendGrid.send(activation_email)
            # inform the user of activation mail sent
            if activation_status == 200:
                new_user_email = new_user.email
                messages.add_message(
                    request, messages.INFO, new_user_email)
            return redirect(reverse('confirm_registration'))

        else:
            args = {}
            args.update(csrf(request))
            return render(request, 'authentication/register.html', {'form': usersignupform})


class ActivateAccountView(View):
    """
    This class handles account activation.
    """

    def get(self, request, *args, **kwargs):
        """Handles GET requests to 'activate_account' named route.

        Returns: A redirect to the login page.
        Raises: A Http404 error.
        """
        # get the activation_hash captured in url
        activation_hash = kwargs['activation_hash']

        # reverse the hash to get the user (auto-authentication)
        user = Hasher.reverse_hash(activation_hash)

        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.save()
                if user.is_active:
                    return redirect(reverse('login'))

        else:
            raise Http404("/User does not exist")


class UserConfirm(TemplateView):
    """
    This class handles account creation confirmation.

    Attributes:
        template_name.
    """
    template_name = 'authentication/confirm.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to 'confirm_registration' named route.

        Returns:
            A rendered template response.
        """
        return render(request, self.template_name)
