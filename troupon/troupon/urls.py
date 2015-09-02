
from django.conf.urls import include, url
from django.contrib import admin
import deals
from account import views

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^deals/', include('deals.urls')),
    url(r'^$', deals.views.HomePage.as_view(), name='homepage'),
    url(r'^', include('account.urls')),
]