from django.conf.urls import include, url
from django.contrib import admin
import deals
import account

urlpatterns = [
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
    url(r'^categories/', include('deals.urls')),
    url(r'^$', deals.views.HomePage.as_view(), name='homepage'),
]
