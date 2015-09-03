from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
      url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
      url(r'^signupreq/$',views.UserSignupreq.as_view(),name = 'UserSignupreq'),
      url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),

      
)