
from django.conf.urls import include, url
from django.contrib import admin
import account 

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'auth^', include('account.urls')),

]
