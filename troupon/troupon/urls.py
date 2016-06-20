import api

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from deals.views import HomePageView

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [

    # home/index:
    url(r'^$', HomePageView.as_view(), name='homepage'),

    # apps:
    url(r'^', include('authentication.urls')),
    url(r'^deals/', include('deals.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^merchant/', include('merchant.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^cart/', include('cart.urls')),

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

    # api routes
    url(r'^api/', include(api)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/login/', obtain_jwt_token),
    #allow user to change ip
    url(r'^geoip/', include('django_geoip.urls')),
]
