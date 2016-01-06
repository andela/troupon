from django.conf.urls import url

from authentication.views import UserLoginView, ForgotPasswordView,\
                          ResetPasswordView, UserRegistrationView,\
                          ActivateAccountView, UserConfirm,\
                          UserLogoutView


urlpatterns = [

    url(r'^register/$',
        UserRegistrationView.as_view(),
        name='register'),

    url(r'^login/$',
        UserLoginView.as_view(),
        name='login'),

    url(r'^logout/$',
        UserLogoutView.as_view(),
        name='logout'),

    url(r'^confirm/$',
        UserConfirm.as_view(),
        name='confirm_registration'),

    url(r'^activation/(?P<activation_hash>([a-z0-9A-Z])+)$',
        ActivateAccountView.as_view(),
        name='activate_account'),

    url(r'^recovery/$',
        ForgotPasswordView.as_view(),
        name='account_forgot_password'),

    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$',
        ResetPasswordView.as_view(),
        name='account_reset_password'),

]
