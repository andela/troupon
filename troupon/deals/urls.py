
from django.conf.urls import url

from .views import DealsView, FilteredDealsView,\
    DealSlugView, DealHaystackSearchView, DealSearchCityView, ReviewView


urlpatterns = [

    # pattern maps to view handling `GET` requests to
    # /deals/
    url(r'^$', DealsView.as_view(), name='deals'),

    # pattern maps to view handling `GET` requests to
    # /deals/<deal_slug>/
    url(r'^(?P<deal_slug>[\w-]+)/$',
        DealSlugView.as_view(),
        name='deal-with-slug'),

    # pattern maps to view handling `GET` requests to
    # /deals/<filter_by>/<filter_slug>/?q=search
    url(r'^(?P<filter_type>[\w-]+)/(?P<filter_slug>[\w-]+)/$',
        FilteredDealsView.as_view(),
        name='deal-filter-with-slug'),

    # pattern maps to view handling `GET` requests to
    # /deals/search?q=<search_key>&city=<city_id>
    url(r'^search$',
        DealSearchCityView.as_view(),
        name='dealsearchcity'),

    # pattern maps to view handling `GET` requests to
    # /deals/search/autosuggest?q=<search_key>
    url(r'^search/autosuggest/$',
        DealHaystackSearchView.as_view(),
        name='dealsearchauto'),

    # pattern maps to view handling `POST` requests to
    # /deals/reviews/submit
    url(r'^reviews/submit$',
        ReviewView.as_view(),
        name='submit-review'),
]
