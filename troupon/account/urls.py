from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
      url(r'^signup/$',views.UserSignupView,name = 'UserSignupView'),
      url(r'^signupreq/$',views.UserSignupreq,name = 'UserSignupreq'),
      url(r'^confirm/$',views.Userconfirm,name = 'Userconfirm'),

      
)