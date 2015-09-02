from django.conf.urls import include, url
from deals.views import Signup, LandingPage

urlpatterns = [
    url(r'^auth/$', Signup.as_view(), name='Signup'),
    url(r'^$', LandingPage.as_view(), name='homepage'),
]
