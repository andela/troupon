from django.conf.urls import url, include
from .views import SingleDealView, DealSearchView, DealSearchCityView


urlpatterns = [
  url(r'^search/', include('haystack.urls')),
  url(r'^search/entry/$', DealSearchView.as_view(), name = 'dealsearch'),
  url(r'^(?P<deal_id>\d+)/$', SingleDealView.as_view(), name='single_deal'),
  url(r'^search/cities/$', DealSearchCityView.as_view(), name ='dealsearchcity')
]
