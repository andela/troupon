from django.conf.urls import url
from .views import SingleDealView,


urlpatterns = [
    url(r'^(?P<deal_id>\d+)/$', SingleDealView.as_view(), name='single_deal'),
]
