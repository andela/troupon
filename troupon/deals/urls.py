
from django.conf.urls import url, include
from .views import DealSearchView, DealSearchCityView, DealView, DealsView


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^search/entry/$', DealSearchView.as_view(), name = 'dealsearch'),
    url(r'^search/cities/$', DealSearchCityView.as_view(), name ='dealsearchcity'),
    url(r'^$', DealsView.as_view(), name='deals'),
    url(r'^(?P<deal_id>[0-9]+)$', DealView.as_view(), name='deal'),

  ]
