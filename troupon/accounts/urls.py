from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.IndexRedirectView.as_view(), name='index'),
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
]