# from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView


# Create your views here.


class Signup(TemplateView):
    template_name = "deals/signin_register.html"


class LandingPage(TemplateView):
    """class that handles display of landing page/homepage"""

    template_name = "deals/landing_page.html"


