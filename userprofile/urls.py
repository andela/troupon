from django.conf.urls import url, include
from .views import Userprofileview

urlpatterns = [
  url(r'^profile/$', Userprofileview.as_view(), name = 'userprofile'),
  
]