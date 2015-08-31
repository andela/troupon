from django.conf.urls import include, url
from deals.views import Signup

urlpatterns = [

    url(r'^auth/$', Signup.as_view(), name = 'Signup'),
]
