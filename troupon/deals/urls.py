from django.conf.urls import url
from .views import DealView


urlpatterns = [
    url(r'^$', DealView.as_view(), name='deal'),
]
