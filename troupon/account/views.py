from django.views.generic.base import View
from django.shortcuts import render, redirect

# Create your views here.

class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hi, This is just a placeholder for forgot_password.html')

     	# context = {
	    #     'search_form': 'placeholder',
	    # }
	    # return render(request, 'webapp/home.html', context)