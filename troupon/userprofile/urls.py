from django.conf.urls import url

from userprofile.views import Userprofileview

urlpatterns = [
    url(r'^(?P<username>\w+)$', Userprofileview.as_view(), name = 'userprofile'),
]