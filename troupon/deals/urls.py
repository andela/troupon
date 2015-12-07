
from django.conf.urls import url, include
from .views import DealsView, FilteredDealsView, DealView, DealSlugView,\
    DealHaystackSearchView, DealSearchCityView


urlpatterns = [

    url(r'^search/', include('haystack.urls')),

    url(r'^search/entry/$',
        DealHaystackSearchView.as_view(),
        name='dealsearch'),

    url(r'^search/cities/$',
        DealSearchCityView.as_view(),
        name='dealsearchcity'),

    # /deals/
    url(r'^$', DealsView.as_view(), name='deals'),

    # /deals/:filter_by/:filter_slug/
    url(r'^(?P<filter_type>[\w-]+)/(?P<filter_slug>[\w-]+)/$',
        FilteredDealsView.as_view(),
        name='deal-filter-with-slug'),

    # /deals/:id/
    url(r'^(?P<deal_id>[0-9]+)/$', DealView.as_view(), name='deal'),

    # /deals/:slug/
    url(r'^(?P<deal_slug>[\w-]+)/$',
        DealSlugView.as_view(),
        name='deal-with-slug'),

]
