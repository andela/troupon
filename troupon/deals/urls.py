from django.conf.urls import url
from .views import DealView, DealsView


urlpatterns = [
    url(r'^$', DealsView.as_view(), name='deals'),
    url(r'^(?P<deal_id>[0-9]+)$', DealView.as_view(), name='deal'),
]
