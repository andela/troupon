from django.conf.urls import url

from .views import DownloadView

urlpatterns = [
    # pattern maps to view handling `GET` requests to
    # /tickets/
    url(r'^(?P<deal_id>([0-9])+)/$',
        DownloadView.as_view(),
        name='download_ticket'),
]
