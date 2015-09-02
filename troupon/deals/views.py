# from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.


class Signup(TemplateView):

    template_name = "deals/signin_register.html"


class LandingPage(TemplateView):
    """class that handles display of landing page/homepage"""

    template_name = "deals/landing_page.html"
    context_var = {'show_subscribe': True}

    def get(self, request):
        return render(request, self.template_name, self.context_var)

