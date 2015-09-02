from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from forms import EmailForm

class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):

        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)


    def post(self, request, *args, **kwargs):

        context = {
            'page_title': 'Forgot Password',
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)