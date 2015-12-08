from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.utils.text import slugify

import cloudinary
from haystack.query import SearchQuerySet

from deals.models import Category, Deal, Advertiser, STATE_CHOICES
from deals.baseviews import DealListBaseView


class HomePageView(DealListBaseView):
    """ View class that handles display of the homepage.
        Overrides the base get method, but still uses
        the base render_deal_list method to get the
        rendered latest deals listing.
    """

    def get(self, request, *args, **kwargs):

        # get the popular categories:
        popular_categories = Category.objects.all()[:12]

        # get the featured deals:
        featured_deals = Deal.objects.filter(featured=True).order_by('pk')[:5]

        # get the latest deals i.e. sorted by latest date:
        latest_deals = Deal.objects.filter(active=True)\
                                   .order_by('date_last_modified')
        list_title = "Latest Deals"
        list_description = "Checkout the hottest new deals from all your favourite brands:"

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            queryset=latest_deals,
            title=list_title,
            description=list_description,
            pagination_base_url=reverse('deals')
        )
        context = {
            'popular_categories': popular_categories,
            'featured_deals': featured_deals,
            'rendered_deal_list': rendered_deal_list
        }
        context.update(csrf(request))
        return TemplateResponse(request, 'deals/index.html', context)


class DealsView(DealListBaseView):
    """ View class that handles display of the deals page.
        Simply configures the options and makes use of the base methods
        to render return latest deals listing.
    """
    queryset = Deal.objects.filter(active=True).order_by('date_last_modified')
    title = "Latest Deals"
    description = "See all the hottest new deals from all your favourite brands:"


class FilteredDealsView(DealListBaseView):
    """ Displays deals filtered by  category, city or merchant.
        Works with routes of the form: '/deals/:filter_type/:filter_slug/'
    """
    category_title_format = "{} deals"
    city_title_format = "Deals in {}"
    advertiser_title_format = "Deals from {}"
    
    category_description_format = "See all the hot new {} deals!"
    city_description_format = "See all the hot new deals in {}!"
    advertiser_description_format = "See all the hot new from {}!"

    def get_queryset(self):
        """ returns the default deals queryset.
            override this method to return custom querysets.
        """
        filter_type = self.kwargs.get('filter_type')
        filter_slug = self.kwargs.get('filter_slug')
        queryset = self.queryset

        if filter_type == 'category':
            category = get_object_or_404(Category, slug=filter_slug)
            self.title = self.category_title_format\
                             .format(category.name)
            self.description = self.category_description_format\
                                   .format(category.name)
            queryset = queryset.filter(category=category)

        elif filter_type == 'merchant':
            advertiser = get_object_or_404(Advertiser, slug=filter_slug)
            self.title = self.advertiser_title_format\
                             .format(advertiser.name)
            self.description = self.advertiser_description_format\
                                   .format(advertiser.name)
            queryset = queryset.filter(advertiser=advertiser)

        elif filter_type == 'city':
            try:
                state = [state for state in STATE_CHOICES
                         if slugify(state[1]) == filter_slug][0]
            except:
                raise Http404('Not found')

            self.title = self.city_title_format\
                             .format(state[1])
            self.description = self.city_description_format\
                                   .format(state[1])
            queryset = queryset.filter(state=state[0])
        else:
            raise SuspiciousOperation('Invalid request')

        return queryset


class DealHaystackSearchView(View):

    ''' Haystack search class for auto complete.'''

    template_name = 'deals/ajax_search.html'

    def get(self, request):
        deals = SearchQuerySet().autocomplete(
            content_auto=request.GET.get('q', '')
        )
        return TemplateResponse(request, self.template_name, {'deals': deals})


class DealSearchCityView(DealListBaseView):

    ''' class to search for deals via title and states'''

    def get(self, request, *args, **kwargs):
        value = request.GET.get('q', '')
        cityquery = int(request.GET.get('city', '25'))
        # get the deal results:
        deals = Deal.objects.filter(title__icontains=value)\
                            .filter(state__icontains=cityquery)

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            queryset=deals,
            title="Search Results",
            zero_items_message = 'Your search - {} - in {} did not match any deals.'\
                                 .format(value, STATE_CHOICES[cityquery-1][1]),
            description='{} deal(s) found for this search.'.format(len(deals))
            # pagination_base_url=reverse('deals')
        )
        context = {
            'rendered_deal_list': rendered_deal_list
        }
        context.update(csrf(request))
        return TemplateResponse(request, 'deals/searchresult.html', context)


class DealSlugView(View):
    """ Respond to routes to deal url using slug
    """
    def get(self, request, *args, **kwargs):
        deal_slug = self.kwargs.get('deal_slug')
        try:
            deal = Deal.objects.filter(slug=deal_slug)
            if len(deal) > 1:
                deal = deal[0]
            else:
                deal = deal[0]
        except (Deal.DoesNotExist, AttributeError):
            raise Http404('Deal with this slug not found!')

        context = {'deal': deal}
        return TemplateResponse(request, 'deals/detail.html', context)


class DealView(View):
    """This handles request for each deal by id.
    """

    def get(self, request, *args, **kwargs):
        deal_id = self.kwargs.get('deal_id')  # get deal_id from request
        if not deal_id:
            deals = Deal.objects.all()
            # engine = Engine.get_default()
            # template = engine.get_template('deals/list.html')
            context = {'deals': deals, }
            # return HttpResponse(template.render(context))
            return TemplateResponse(request, 'deals/list.html', context)
        # get and return the page for the single deal
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            raise Http404('Deal does not exist')

        context = {'deal': deal, }
        return TemplateResponse(request, 'deals/detail.html', context)

    def post(self, request, *args, **kwargs):
        """ Upload a deal photo to cloudinary then creates deal
        """
        title = self.kwargs.get('title')
        photo = request.FILES.get('photo')
        self.upload(photo, title)
        return redirect(reverse('deals'))

    def upload(self, file, title):
        """ Upload deal photo to cloudinary
        """
        return cloudinary.uploader.upload(
            file,
            public_id=title
        )
