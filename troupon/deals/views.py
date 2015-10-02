from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from deals.models import Deal, STATE_CHOICES
from django.template import Engine, RequestContext
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator


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

class DealSearchView(View):

    template_name = 'deals/ajax_search.html'

    def post(self,request):
        deals = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))
        return render(request, self.template_name, {'deals': deals})

class DealSearchCityView(View):

    template_name = 'deals/searchresult.html' #template for multiple deals with pagination comes here

    def get(self,request):

        city_list = Deal.objects.filter(title__contains=request.GET.get('title', '')).filter(deal_state__contains=request.GET.get('deal_state', ''))
        paginator = Paginator(city_list, 4)

        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            cities = paginator.page(page)
        except(EmptyPage, InvalidPage):
            cities = paginator.page(paginator.num_pages)

        return render_to_response(self.template_name, { 'cities' : cities }, context_instance=RequestContext(request))
        #deal_state and title from html page......
