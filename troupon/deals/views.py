from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from django.template import Engine, RequestContext, loader
from django.core.paginator import Paginator
from django.core.context_processors import csrf

from deals.models import Category, Deal, STATE_CHOICES, EPOCH_CHOICES

import cloudinary


class DealListBaseView(View):
    
    deals = []
    title = "Deals"
    description = ""
    zero_items_message = "Sorry, no deals found!"
    num_page_items = 15
    min_orphan_items = 2
    show_page_num = 1
    pagination_base_url = ""
    date_filter = { 'choices': EPOCH_CHOICES, 'default': 0 }

        
    def render_deal_list(self, request, deals, **kwargs):

        # update the default options with any specified as kwargs:
        for arg_name in kwargs:
            try:
                setattr(self, arg_name, kwargs.get(arg_name))
            except:
                pass

        # paginate deals and get the specified page:
        paginator = Paginator(
            deals, 
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


    def get(self, request, *args, **kwargs):

        context = {
            'rendered_deal_list': self.render_deal_list(request, self.deals),
            'search_options': {
                'query': "",
                'states': { 'choices': STATE_CHOICES, 'default': 25 },
            }
        }
        return render(request, 'deals/deal_list_base.html', context)




class HomePageView(DealListBaseView):
    """class that handles display of the homepage"""

    def get(self, request, *args, **kwargs):

        # get the popular categories:
        popular_categories = Category.objects.all()[:12]

        # get the featured deals:
        featured_deals = Deal.objects.filter(featured=True).order_by('pk')[:5]

        # get the latest deals i.e. sorted by latest date:
        latest_deals = Deal.objects.all().order_by('date_last_modified')
        list_title = "Latest Deals"
        list_description = "Checkout the hottest new deals from all your favourite brands:"

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request, 
            latest_deals, 
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

    deals = Deal.objects.all().order_by('date_last_modified')
    title = "Latest Deals"
    description = "See all the hottest new deals from all your favourite brands:"
    num_page_items = 10




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
