from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('deals.urls')),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
]
