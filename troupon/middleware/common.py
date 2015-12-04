
from django.conf import settings
from deals.models import Category, Advertiser, STATE_CHOICES


class CommonContextMiddleware(object):
    """
    Middleware class that injects common data that's needed
    when rendering most of view responses into the context
    of the template_response objects returned by the views.
    The injected data includes:

    cities: includes a paginated listing of all state
                   choices/cities available on the site.
    categories : includes a paginated listing of all categories
                 available on the site.
    advertisers: includes a paginated listing of all advertisers
                 available on the site.
    search_options : includes any current search query and the
                     default state choice for searches.
    """

    def process_template_response(self, request, response):
        """
        Middleware hook method called immediately after the
        view function returns a response.
        """
        response.context_data.update({
            'cities': STATE_CHOICES,
            'categories': Category.objects.all(),
            'advertisers': Advertiser.objects.all(),
            'search_options': {
                'query': request.GET.get('q', ''),
                'default_city': settings.DEALS.get('default_search_city', 25),
            },
        })
        return response
