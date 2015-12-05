from django.shortcuts import redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.core.context_processors import csrf

import cloudinary
from haystack.query import SearchQuerySet

from deals.models import Category, Deal, Advertiser, STATE_CHOICES
from deals.baseviews import DealListBaseView, CollectionsBaseView, \
                            DealCollectionItemsListBaseView


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
            deals=latest_deals,
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

    deals = Deal.objects.filter(active=True).order_by('date_last_modified')
    title = "Latest Deals"
    description = "See all the hottest new deals from all your favourite brands:"


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


class DealSearchView(View):

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
            deals=deals,
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


class DealCategoryView(DealCollectionItemsListBaseView):
    """ Respond to routes to deal categories using slug
    """
    slug_name = 'category_slug'
    filter_field = 'category'
    model = Category
    not_found = 'Category not found!'
    template = 'deals/deal_list_base.html'

    def get(self, *args, **kwargs):
        self.filter_deals(**{
            self.filter_field: self.get_queryset(
                self.kwargs.get(self.slug_name)
            )
        })
        self.set_title('Latest Deals in {}'.format(self.queryset.name))
        self.set_description(
            'See all the hottest new deals in {}'.format(self.queryset.name)
        )
        return self.do_render()


class CategoryView(CollectionsBaseView):
    """ Lists all categories
    """
    zero_items_message = "Sorry, no categories found!"
    num_page_items = 9
    min_orphan_items = 3
    show_page_num = 1
    pagination_base_url = ""
    queryset = Category.objects.all()
    template = 'deals/categories.html'
    title = "Category Listing for All Available Deals"
    description = "See all categories to choose from"


class AdvertiserView(CollectionsBaseView):
    """ Lists all merchants
    """
    zero_items_message = "Sorry, no merchants were found!"
    num_page_items = 9
    min_orphan_items = 3
    show_page_num = 1
    pagination_base_url = ""
    queryset = Advertiser.objects.all()
    template = 'deals/merchants.html'
    title = "All Merchants with Deals for You"
    description = "See all merchants with great deal offers"


class DealAdvertiserView(DealCollectionItemsListBaseView):
    """ Renders list of deals by an advertiser
    """
    slug_name = 'advertiser_slug'
    filter_field = 'advertiser'
    model = Advertiser
    not_found = 'Merchant not found!'
    template = 'deals/deal_list_base.html'

    def get(self, *args, **kwargs):
        self.filter_deals(**{
            self.filter_field: self.get_queryset(
                self.kwargs.get(self.slug_name)
            )
        })
        self.set_title('Latest Deals in {}'.format(self.queryset.name))
        self.set_description(
            'See all the hottest new deals in {}'.format(self.queryset.name)
        )
        return self.do_render()
