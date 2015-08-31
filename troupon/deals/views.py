#from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView


# Create your views here.


class Signup(TemplateView):
    template_name = "signin_register.html"

