import datetime

from django.views.generic import View
from django.http import Http404
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from deals.models import Deal, EPOCH_CHOICES


class DealListBaseView(View):
    """
    Base class for other Deal listing views.
    It implements a default 'get' method allowing
    subclassing views to render fully functional
    deal listings by simply overriding the default
    class level options.

    Subclassing views can still override and implement
    their own get or post methods. However these methods
    can call the base 'render_deal_list' method which
    returns the rendered deal list as a string.
    """

    # default deal list options as class level vars:
    queryset = Deal.objects.all()  # can be any queryset of Deal instances *
    title = "Deals"
    description = ""
    zero_items_message = "Sorry, no deals found!"
    num_page_items = settings.DEALS.get('num_page_items', 15)
    min_orphan_items = settings.DEALS.get('min_orphan_items', 2)
    show_page_num = 1
    pagination_base_url = ""
    date_filter = {
        'choices': EPOCH_CHOICES,
        'default': -1
    }

    def render_deal_list(self, request, **kwargs):
        """ Takes a queryset of of deal
        """

        # update the default options with any specified as kwargs:
        for arg_name in kwargs:
            try:
                setattr(self, arg_name, kwargs.get(arg_name))
            except:
                pass

        # use date filter parameter to filter deals if specified:
        deals = self.filter_queryset_from_params(
            request,
            self.get_queryset()
        )

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
        deals_listing = {
            'deals_page': deals_page,
            'date_filter': self.date_filter,
            'title': self.title,
            'description': description,
            'pagination_base_url': self.pagination_base_url,
        }

        # set the context and render the template to a string:
        deals_list_context = RequestContext(
            request,
            {'listing': deals_listing}
        )
        template = loader.get_template('snippet_deal_listing.html')
        rendered_template = template.render(deals_list_context)

        #  return the rendered template string:
        return rendered_template

    def filter_queryset_from_params(self, request, queryset):
        """
        uses any date filter parameter specified
        in the query string to filter deals.
        """

        date_filter_param = request.GET.get('dtf')
        if not date_filter_param:
            return queryset

        try:
            date_filter_param = int(date_filter_param)
        except:
            return queryset

        choices = self.date_filter.get('choices', [])
        if date_filter_param < 0 or date_filter_param >= len(choices):
            return queryset

        date_filter_delta = choices[date_filter_param][0]
        if date_filter_delta != -1:
            filter_date = datetime.date.today()\
             - datetime.timedelta(days=date_filter_delta)
            queryset = queryset.filter(
                date_last_modified__gt=filter_date
            )
        self.date_filter['default'] = date_filter_delta
        return queryset

    def get_queryset(self):
        """ returns the default deals queryset.
            override this method to return custom querysets.
        """
        return self.queryset

    def get(self, request, *args, **kwargs):
        """ returns a full featured deals-listing page showing
            the deals set in 'deals' class variable.
        """
        context = {
            'rendered_deal_list': self.render_deal_list(request),
        }
        return TemplateResponse(request, 'deals/deal_list_base.html', context)
