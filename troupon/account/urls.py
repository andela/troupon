from django.conf.urls import url
from account.views import UserSigninView, UserSignoutView,\
    ForgotPasswordView, ResetPasswordView, UserSignupView, Userconfirm

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view(), name='signin'),
    url(r'^signout/$', UserSignoutView.as_view(), name='signout'),
    url(r'^recovery/$', ForgotPasswordView.as_view(), name='account_forgot_password'),
    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$', ResetPasswordView.as_view(), name='account_reset_password'),
    url(r'^signup/$',UserSignupView.as_view(),name = 'UserSignupView'),
    url(r'^confirm/$',Userconfirm.as_view(),name = 'Userconfirm'),
]
