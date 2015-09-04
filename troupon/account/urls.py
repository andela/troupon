from django.conf.urls import patterns, include, url
from account.views import UserSigninView
from account import views

urlpatterns = patterns('',
    url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
    url(r'^signupreq/$',views.UserSignupreq.as_view(),name = 'UserSignupreq'),
    url(r'^signin/$', UserSigninView.as_view()),
    url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),

      
)
