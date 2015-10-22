from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from django.template import Engine, RequestContext, loader
from django.core.paginator import Paginator
from django.core.context_processors import csrf
import datetime
import cloudinary

from deals.models import Category, Deal, STATE_CHOICES, EPOCH_CHOICES


class DealListBaseView(View):
    """ Base class for other Deal listing views.
        It implements a default get method allowing subclassing views to 
        render fully functional deal listings by simply overriding the 
        default class level options.

        Subclassing views can still override and implement their own get or post
        methods. However these methods can call the base 'render_deal_list' method
        which returns the rendered deal list as a string.
    """

    # default deal list options as class level vars:

    deals = Deal.objects.all()  # can any queryset of Deal instances
    title = "Deals"
    description = ""
    zero_items_message = "Sorry, no deals found!"
    num_page_items = 15
    min_orphan_items = 2
    show_page_num = 1
    pagination_base_url = ""
    date_filter = { 'choices': EPOCH_CHOICES, 'default': -1 }

        
    def render_deal_list(self, request, **kwargs):

        # update the default options with any specified as kwargs:
        for arg_name in kwargs:
            try:
                setattr(self, arg_name, kwargs.get(arg_name))
            except:
                pass

        # use date filter parameter to filter deals if specified:
        self.filter_deals_from_params(request)

        # paginate deals and get the specified page:
        paginator = Paginator(
            self.deals, 
            self.num_page_items,
            self.min_orphan_items,
        )
        try:
            # get the page number if present in request.GET
            show_page_num = request.GET.get('pg')
            if not show_page_num:
                show_page_num = self.show_page_num
            deals_page = paginator.page(show_page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver first page.
            deals_page = paginator.page(1)
        except EmptyPage:
            # if page is out of range, deliver last page of results.
            deals_page = paginator.page(paginator.num_pages)

        # set the description to be used in the list header:
        if deals_page.paginator.count:
            description = self.description
        else:
            description = self.zero_items_message

        # combine them all into listing dictionary:
        deals_listing =  {
            'deals_page': deals_page,
            'date_filter': self.date_filter,
            'title': self.title,
            'description': description,
            'pagination_base_url': self.pagination_base_url,
        }

        # set the context and render the template to a string:
        deals_list_context = RequestContext( request, { 'listing': deals_listing } )
        template = loader.get_template('snippet_deal_listing.html')
        rendered_template = template.render(deals_list_context)
                    
        #  return the rendered template string:
        return rendered_template


    def filter_deals_from_params(self, request):
        """ uses any date filter parameter specified in the query string to filter deals.
        """

        date_filter_param = request.GET.get('dtf')
        if not date_filter_param:
            return

        try:
            date_filter_param = int(date_filter_param)
        except:
            return

        choices = self.date_filter.get('choices', [])
        if date_filter_param < 0 or date_filter_param >= len(choices):
            return

        date_filter_delta = choices[date_filter_param][0]
        if date_filter_delta != -1:
            filter_date = datetime.date.today() - datetime.timedelta(days=date_filter_delta)
            self.deals = self.deals.filter(date_last_modified__gt=filter_date)
        
        self.date_filter['default'] = date_filter_delta


    def get(self, request, *args, **kwargs):
        """ returns a full featured deals-listing page s2howing
            the deals set in 'deals' class variable.
        """
        context = {
            'rendered_deal_list': self.render_deal_list(request),
            'search_options': {
                'query': "",
                'states': { 'choices': STATE_CHOICES, 'default': 25 },
            }
        }
        return render(request, 'deals/deal_list_base.html', context)




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
            pagination_base_url=reverse('deals'),
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
        return render(request, 'deals/index.html', context)




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
