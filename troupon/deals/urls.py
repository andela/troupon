from django.conf.urls import url
from .views import DealView


urlpatterns = [
    url(r'^(?P<deal_id>[0-9]+)?$', DealView.as_view(), name='deal'),
]
