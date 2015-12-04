from django.conf.urls import url
from .views import DispatchView, \
    ReadView, ReadFromUserView, ReadDetailView


urlpatterns = [
    url(r'^(?P<action>\w+)/$', DispatchView.as_view(), name='send_message'),
    url(r'^read/(?P<sender>\w+)/$',
        ReadFromUserView.as_view(),
        name='read_user_message'),  # read messages from a user
    url(r'^read/(?P<id>\d+)/(?P<slug>[\w-]+)/$',
        ReadDetailView.as_view(),
        name='read_message'),  # read messages by slug
    url(r'^read$', ReadView.as_view(), name='read_messages'),
]
