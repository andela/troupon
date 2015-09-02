from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePage(TemplateView):
    """class that handles display of the homepage"""

    template_name = "deals/index.html"
    context_var = {'show_subscribe': True}

    def get(self, request):
        return render(request, self.template_name, self.context_var)
