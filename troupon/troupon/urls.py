from django.conf.urls import include, url
from django.contrib import admin
import deals
import account
from deals.views import AboutView, InvestorView, TeamView, SupportView


urlpatterns = [
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
    url(r'^$', deals.views.HomePageView.as_view(), name='homepage'),
    url(r'^about/', AboutView.as_view(), name='about'),
    url(r'^investors/', InvestorView.as_view(), name='investor'),
    url(r'^team/', TeamView.as_view(), name='team'),
    url(r'^support/', SupportView.as_view(), name='support'),
]
