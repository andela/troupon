from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from forms import EmailForm

class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse('Hi, This is just a placeholder for forgot_password.html')
        context = {
            'email_form': EmailForm(auto_id=True),
        }
        return render(request, 'account/forgot_password.html', context)


    def post(self, request, *args, **kwargs):

        return HttpResponse('Hi, This is just a placeholder for forgot_password_mail.html')