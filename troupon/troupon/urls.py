
from django.conf.urls import include, url
from django.contrib import admin
from deals import views
from auth import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
]
