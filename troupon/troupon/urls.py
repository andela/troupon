
from django.conf.urls import include, url
from django.contrib import admin
from deals import views
from auth import deals

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('deals.urls')),
    url(r'^', include('auth.urls')),

]
