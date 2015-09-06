
from django.conf.urls import include, url
from django.contrib import admin
import deals
from account import views
import account 

urlpatterns = [
    url(r'^auth/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
    url(r'^$', deals.views.HomePage.as_view(), name='homepage'),
]
