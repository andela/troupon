from django.conf.urls import include, url
from account.views import UserSigninView

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view()),
    url(r'^account/recovery/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^account/recovery/(?P<recovery_hash>([a-z]|[0-9]|[A-Z])+)/$', ResetFromEmailView.as_view(), name='reset_from_email'),
]