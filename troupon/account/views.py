from django.views.generic import View
from django.contrib import auth
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect

import re

# Create your views here.


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
            user = auth.authenticate(username=email, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(self.request, user)

                # Redirect to a success page.
                referer_view = self.get_referer_view(self.request)

                return HttpResponseRedirect(referer_view, '/deals/')
            else:
                # Show an error page
                data = {'msg': {'content': self.cls_default_msgs['invalid_param']}}
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
