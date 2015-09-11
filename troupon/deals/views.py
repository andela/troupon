from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from deals.models import Deal
from django.template import Template, Context


# Create your views here.
class HomePage(TemplateView):
    """class that handles display of the homepage"""

    template_name = "deals/index.html"
    context_var = {'show_subscribe': True}

    def get(self, request):
        return render(request, self.template_name, self.context_var)


class SingleDealView(View):
    cls_default_msg = {
                        "result": "We're still working on this deal for you.",
                      }  # Default message display when deal's not found

    def get(self, *args, **kwargs):
        deal_id = self.kwargs.get('deal_id')
        try:
            deal = Deal.objects.get(id=deal_id)
            result = {"result": deal}
        except Deal.DoesNotExist:
            result = SingleDealView.cls_default_msg
        template_stub = Template("{{result}}")
        return HttpResponse(template_stub.render(Context(result)))
