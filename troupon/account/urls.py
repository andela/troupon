<<<<<<< HEAD

from django.conf.urls import patterns, include, url
from account.views import UserSigninView
from account import views

urlpatterns = patterns('',
    url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
    url(r'^signupreq/$',views.UserSignupreq.as_view(),name = 'UserSignupreq'),
    url(r'^signin/$', UserSigninView.as_view()),
    url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),

      
)
=======
from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
      url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
      url(r'^signupreq/$',views.UserSignupreq.as_view(),name = 'UserSignupreq'),
      url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),

      
)
>>>>>>> d432157acd84c8463a4b053243f2273e62e72c25
