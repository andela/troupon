from django.conf.urls import url
from account.views import UserSigninView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view(), name='signin'),
    url(r'^account/recovery/$', ForgotPasswordView.as_view(), name='account_forgot_password'),
    url(r'^account/recovery/(?P<recovery_hash>([abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ])+)$',
    	ResetPasswordView.as_view(), 
    	name='account_reset_password'
    ),
]