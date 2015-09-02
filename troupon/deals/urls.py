from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='homepage'),
]
