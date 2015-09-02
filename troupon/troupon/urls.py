
from django.conf.urls import include, url
from django.contrib import admin
from deals import views
from account import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('account.urls')),

]
