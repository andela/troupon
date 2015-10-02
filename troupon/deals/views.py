from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from deals.models import Deal, STATE_CHOICES
from django.template import Engine, RequestContext


# Create your views here.
class HomePage(TemplateView):
    """class that handles display of the homepage"""

    template_name = "deals/index.html"
    context_var = {
        'show_subscribe': False,
        'show_search': True,
        'states': { 'choices': STATE_CHOICES,  'default': 25 }
    }

    def get(self, request):
        return render(request, self.template_name, self.context_var)


class SingleDealView(View):
    """This handles request for each deal by id.
    """

    def get(self, *args, **kwargs):
        deal_id = self.kwargs.get('deal_id')  # get deal_id from request
        try:
            deal = Deal.objects.get(id=deal_id)
            result = {"result": deal}
        except Deal.DoesNotExist:
            raise Http404('Deal does not exist')

        # Replace template object compiled from template code
        # with an application template.
        # Use Engine.get_template(template_name)
        engine = Engine.get_default()
        t = engine.from_string('{{result}}')

        # set result in RequestContext
        c = RequestContext(self.request, result)
        return HttpResponse(t.render(c))
