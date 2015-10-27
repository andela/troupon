from django.conf.urls import url
from account.views import UserSigninView, ForgotPasswordView, ResetPasswordView,UserSignupView,ActivateAccountView, Userconfirm, Userprofileview, UserChangePassword

urlpatterns = [
    url(r'^signin/$', UserSigninView.as_view(), name='signin'),
    url(r'^recovery/$', ForgotPasswordView.as_view(), name='account_forgot_password'),
    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$', ResetPasswordView.as_view(), name='account_reset_password'),
    url(r'^signup/$',UserSignupView.as_view(),name = 'UserSignupView'),
    url(r'^activation/(?P<activation_hash>([a-z0-9A-Z])+)$', ActivateAccountView.as_view(), name='activate_account'),
    url(r'^confirm/$',Userconfirm.as_view(),name = 'Userconfirm'),
    url(r'^profile/user/(?P<username>\w+)$', Userprofileview.as_view(), name = 'userprofile'),
    url(r'^changepassword/(?P<username>\w+)$', UserChangePassword.as_view(), name = 'changepassword'),

]


