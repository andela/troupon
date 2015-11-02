from django.shortcuts import render,render_to_response,redirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from deals.models import Deal, STATE_CHOICES
from django.template import Engine, RequestContext, loader
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator
from django.core.context_processors import csrf
from deals.models import Category, Deal, STATE_CHOICES, EPOCH_CHOICES
from deals.baseviews import DealListBaseView

import datetime
import cloudinary


class HomePageView(DealListBaseView):
    """ View class that handles display of the homepage. 
        Overrides the base get method, but still uses the base render_deal_list method
        to get the rendered latest deals listing.
    """

    def get(self, request, *args, **kwargs):

        # get the popular categories:
        popular_categories = Category.objects.all()[:12]

        # get the featured deals:
        featured_deals = Deal.objects.filter(featured=True).order_by('pk')[:5]

        # get the latest deals i.e. sorted by latest date:
        latest_deals = Deal.objects.filter(active=True).order_by('date_last_modified')
        list_title = "Latest Deals"
        list_description = "Checkout the hottest new deals from all your favourite brands:"

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            deals=latest_deals,
            title=list_title, 
            description=list_description,
            pagination_base_url=reverse('deals')
        )
        context = {
            'search_options': {
                'query': "",
                'states': { 'choices': STATE_CHOICES, 'default': 25 },
            },
            'popular_categories': popular_categories,
            'featured_deals': featured_deals,
            'rendered_deal_list': rendered_deal_list
        }
        context.update(csrf(request))
        return render(request,'deals/index.html', context)


class DealsView(DealListBaseView):
    """ View class that handles display of the deals page. 
        Simply configures the options and makes use of the base methods 
        to render return latest deals listing.
    """

    deals = Deal.objects.filter(active=True).order_by('date_last_modified')
    title = "Latest Deals"
    description = "See all the hottest new deals from all your favourite brands:"


class DealView(View):
    """This handles request for each deal by id.
    """

    def get(self, *args, **kwargs):
        deal_id = self.kwargs.get('deal_id')  # get deal_id from request
        if not deal_id:
            deals = Deal.objects.all()
            engine = Engine.get_default()
            template = engine.get_template('deals/list.html')
            context = RequestContext(self.request, {'deals': deals})
            return HttpResponse(template.render(context))
        try:
            deal = Deal.objects.get(id=deal_id)
            deal = {'deal': deal}
        except Deal.DoesNotExist:
            raise Http404('Deal does not exist')

        # Replace template object compiled from template code
        # with an application template.
        # Use Engine.get_template(template_name)
        engine = Engine.get_default()
        template = engine.get_template('deals/detail.html')

        # set result in RequestContext
        context = RequestContext(self.request, deal)
        return HttpResponse(template.render(context))


    def post(self, request):
        """This handles creation of deals
        """
        try:
            deal = Deal(request.POST)
            response = self.upload(request.FILES, request.POST.get('title'))
            deal.photo_url = response.get('public_url')
            deal.save()
            return redirect('/deals/{0}/'.format(deal.id))
        except:
            return redirect('/deals/')

    def upload(self, file, title):
        return cloudinary.uploader.upload(
                file,
                public_id=title
            )


class DealSearchView(View):

    template_name = 'deals/ajax_search.html'

    def post(self,request):
        deals = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))
        return render(request, self.template_name, {'deals': deals})


class DealSearchCityView(View):

    template_name = 'deals/searchresult.html' 

    def get(self,request):

        city_list = Deal.objects.filter(title__contains=request.GET.get('q', '')).filter(deal_state__contains=request.GET.get('city', ''))
        paginator = Paginator(city_list, 4)

        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            cities = paginator.page(page)
        except(EmptyPage, InvalidPage):
            cities = paginator.page(paginator.num_pages)

        stitle=request.GET.get('q', '')

        args = {
        'show_search': True,
        'states': { 'choices': STATE_CHOICES,  'default': 25 },
        'cities':cities,
        'stitle':stitle
    }

        return render_to_response(self.template_name, args, context_instance=RequestContext(request))
