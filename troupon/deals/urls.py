from django.conf.urls import url
from .views import SingleDealView, DealSearchView 


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^search/entry/$', DealSearchView.as_view(), name = 'dealsearch'),
    url(r'^(?P<deal_id>\d+)/$', SingleDealView.as_view(), name='singledeal'),
]
