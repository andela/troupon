from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from deals.views import HomePageView

urlpatterns = [

    # home/index:
    url(r'^$', HomePageView.as_view(), name='homepage'),

    # apps:
    url(r'^', include('authentication.urls')),
    url(r'^deals/', include('deals.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^merchant/', include('messages.urls')),

    # static pages:
    url(r'^about/',
        TemplateView.as_view(template_name="about.html"),
        name='about'),

    url(r'^investors/',
        TemplateView.as_view(template_name="investor.html"),
        name='investor'),

    url(r'^team/',
        TemplateView.as_view(template_name="team.html"),
        name='team'),

    url(r'^support/',
        TemplateView.as_view(template_name="support.html"),
        name='support'),

    # admin:
    url(r'^admin/', include(admin.site.urls)),

    # third party apps:
    url(r'^accounts/', include('allaccess.urls')),

]
