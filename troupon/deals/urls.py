
from django.conf.urls import url, include
from .views import DealSearchView, DealSearchCityView, DealView, DealsView, \
        , CategoryView, DealCategoryView, DealSlugView


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^search/entry/$', DealSearchView.as_view(), name = 'dealsearch'),
    url(r'^search/cities/$', DealSearchCityView.as_view(), name ='dealsearchcity'),
    url(r'^$', DealsView.as_view(), name='deals'),
    # /deals/87
    url(r'^(?P<deal_id>[0-9]+)$', DealView.as_view(), name='deal'),
    # /deals/87/spa-treatment-discount
    url(r'^(?P<deal_id>[0-9]+)/(?P<deal_slug>[\w-]+)/$',
        DealSlugView.as_view(),
        name='deal-with-slug'),
    url(r'^listings/$',
        DealCategoryView.as_view(),
        name='deal-category-with-slug'),
    url(r'^categories/$',
        CategoryView.as_view(),
        name='deal-categories'),
    url(r'^categories/$', DealSlugView.as_view(), name='deal-categories'),
]
