from django.conf.urls import patterns, include, url
from account.views import UserSigninView
from account import views

urlpatterns = patterns('',
    url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
    url(r'^signuprequest/$',views.UserSignupRequest.as_view(),name = 'UserSignupRequest'),
    url(r'^signin/$', UserSigninView.as_view()),
    url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),

      
)
