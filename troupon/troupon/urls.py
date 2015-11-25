from django.conf.urls import include, url
from django.contrib import admin
import deals
import account
import userprofile
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deals/', include('deals.urls')),
    url(r'^userprofile/', include('userprofile.urls')),
    url(r'^$', deals.views.HomePageView.as_view(), name='homepage'),
    url(r'^about/', TemplateView.as_view(template_name="deals/about.html"), name='about'),
    url(r'^investors/', TemplateView.as_view(template_name="deals/investor.html"), name='investor'),
    url(r'^team/', TemplateView.as_view(template_name="deals/team.html"), name='team'),
    url(r'^support/', TemplateView.as_view(template_name="deals/support.html"), name='support'),
]
