from django.shortcuts import render,render_to_response


# Create your views here.

def signup(request):
    return render_to_response('signin_register.html')
