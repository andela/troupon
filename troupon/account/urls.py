from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
      url(r'^signup/$',views.UserSignin,name = 'UserSignup'),
      url(r'^signupreq/$',views.UserSignin,name = 'UserSignupreq'),
      url(r'^confirm/$',views.Userconfirm,name = 'Userconfirm'),

      
)