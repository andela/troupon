from django.conf.urls import url

from views import UserProfileView

urlpatterns = [

    url(r'^$',
        UserProfileView.as_view(),
        name='account'),

    url(r'^profile/$',
        UserProfileView.as_view(),
        name='userprofile'),

]
