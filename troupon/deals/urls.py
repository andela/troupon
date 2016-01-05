
from django.conf.urls import url

from .views import DealsView, FilteredDealsView,\
    DealSlugView, DealSearchCityView,\
    DealHaystackSearchView


urlpatterns = [

    # /deals/
    url(r'^$', DealsView.as_view(), name='deals'),

    # /deals/:slug/
    url(r'^(?P<deal_slug>[\w-]+)/$',
        DealSlugView.as_view(),
        name='deal-with-slug'),

    # /deals/:filter_by/:filter_slug/?q=search
    url(r'^(?P<filter_type>[\w-]+)/(?P<filter_slug>[\w-]+)/$',
        FilteredDealsView.as_view(),
        name='deal-filter-with-slug'),

    # /deals/search?q=<search_key>&city=<city_id>
    url(r'^search$',
        DealSearchCityView.as_view(),
        name='dealsearchcity'),

    # /deals/search/autosuggest?q=<search_key>
    url(r'^search/autosuggest/$',
        DealHaystackSearchView.as_view(),
        name='dealsearchauto'),
]
