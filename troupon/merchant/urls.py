from django.conf.urls import url
from conversations.views import MessagesView, MessageView

urlpatterns = [
    # pattern maps to view handling `POST` and `GET`
    #  requests to `/merchant/messages`
    url(
        r'^messages/$',
        MessagesView.as_view(),
        name='messages'
    ),

    # pattern maps to view handling `POST` and `GET`
    #  requests to `/merchant/messages/<m_id>`
    url(
        r'^message/(?P<m_id>[0-9]+)/$',
        MessageView.as_view(),
        name='message'
    ),
]
