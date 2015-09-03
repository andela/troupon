from django.conf.urls import url
from account.views import UserSigninView, ForgotPasswordView, ResetPasswordView,UserSignupView,Userconfirm

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view(), name='signin'),
    url(r'^recovery/$', ForgotPasswordView.as_view(), name='account_forgot_password'),
    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$', ResetPasswordView.as_view(), name='account_reset_password'),
    url(r'^signup/$', UserSignupView,name = 'UserSignupView'),
    url(r'^confirm/$', Userconfirm,name = 'Userconfirm'),

<<<<<<< HEAD
]
=======
urlpatterns = patterns('',
      url(r'^signup/$',views.UserSignupView.as_view(),name = 'UserSignupView'),
      url(r'^signupreq/$',views.UserSignupreq.as_view(),name = 'UserSignupreq'),
      url(r'^confirm/$',views.Userconfirm.as_view(),name = 'Userconfirm'),
>>>>>>> [#102560626] using instantiated class of Mysignuform

