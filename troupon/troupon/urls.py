
from django.conf.urls import include, url
from django.contrib import admin
<<<<<<< HEAD
import deals
from account import views
import account 
=======
>>>>>>> d432157acd84c8463a4b053243f2273e62e72c25

urlpatterns = [
    url(r'^auth/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^deals/', include('deals.urls')),
    url(r'^$', deals.views.HomePage.as_view(), name='homepage'),
=======
    url(r'^auth/', include('account.urls')),

>>>>>>> d432157acd84c8463a4b053243f2273e62e72c25
]
