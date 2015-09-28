from django.conf.urls import url
from .views import SingleDealView, DealsByCategoryView


urlpatterns = [
    url(r'^(?P<deal_id>\d+)/$', SingleDealView.as_view(), name='single_deal'),
    url(r'^(?P<category_id>\d+)/(?P<category_name>\w+)/$',
        DealsByCategoryView.as_view()),
]
