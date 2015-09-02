from django.conf.urls import include, url
from account.views import UserSigninView

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view()),
	url(r'^account/forgot_password/$', ForgotPasswordView.as_view(), name='forgot_password'),
]