from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView, TemplateView

# Create your views here.

class IndexRedirectView(RedirectView):
    permanent = True
    pattern_name = 'accounts:settings'

class SettingsView(TemplateView):
    template_name = "accounts/settings.html"

class ProfileView(TemplateView):
    template_name = "accounts/settings.html"

# class HistoryView(TemplateView):
#     template_name = "accounts/settings.html"
