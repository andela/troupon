from django.conf.urls import url

from userprofile.views import Userprofileview

urlpatterns = [
url(r'^user/(?P<username>\w+)$', Userprofileview.as_view(), name = 'userprofile'),
]