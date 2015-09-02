from django.conf.urls import include, url
from account.views import UserSigninView

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view()),
]