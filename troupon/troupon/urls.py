
from django.conf.urls import include, url
from django.contrib import admin
import deals
from auth import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
    url(r'^$', deals.views.HomePage.as_view(), name='homepage'),
]
