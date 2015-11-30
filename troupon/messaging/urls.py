from django.conf.urls import url
from .views import PostManDispatchView, PostManReadView, PostManReadFromUserView


urlpatterns = [
    url(r'^(?P<action>\w+)/$', PostManDispatchView.as_view(), name='send_message'),
    url(r'^read/(?P<sender>\w+)/$', PostManReadFromUserView.as_view(), name='read_user_message'),
    url(r'^read$', PostManReadView.as_view(), name='read_message'),
]
