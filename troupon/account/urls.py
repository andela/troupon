from django.conf.urls import url
from account.views import UserSigninView, ForgotPasswordView, ResetPasswordView,UserSignupView,Userconfirm

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view(), name='signin'),
    url(r'^recovery/$', ForgotPasswordView.as_view(), name='account_forgot_password'),
    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$', ResetPasswordView.as_view(), name='account_reset_password'),
    url(r'^signup/$', UserSignupView,name = 'UserSignupView'),
    url(r'^confirm/$', Userconfirm,name = 'Userconfirm'),

]

