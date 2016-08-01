from django.conf.urls import url

from authentication.views import UserLoginView, ForgotPasswordView,\
                          ResetPasswordView, UserRegistrationView,\
                          ActivateAccountView, UserConfirm,\
                          UserLogoutView


urlpatterns = [

    # pattern maps to view handling `GET` and `POST` requests to
    # /register/
    url(r'^register/$',
        UserRegistrationView.as_view(),
        name='register'),

    # pattern maps to view handling `GET` and `POST` requests to
    # /login/
    url(r'^login/$',
        UserLoginView.as_view(),
        name='login'),

    # pattern maps to view handling `GET` requests to
    # /logout/
    url(r'^logout/$',
        UserLogoutView.as_view(),
        name='logout'),

    # pattern maps to view handling `GET` requests to
    # /confirm/
    url(r'^confirm/$',
        UserConfirm.as_view(),
        name='confirm_registration'),

    # pattern maps to view handling `GET` requests to
    # /activation/<activation_hash>
    url(r'^activation/(?P<activation_hash>([a-z0-9A-Z])+)$',
        ActivateAccountView.as_view(),
        name='activate_account'),

    # pattern maps to view handling `GET` requests to
    # /recovery/
    url(r'^recovery/$',
        ForgotPasswordView.as_view(),
        name='account_forgot_password'),

    # pattern maps to view handling `GET` requests to
    # /recovery/<recovery_hash>/
    url(r'^recovery/(?P<recovery_hash>([a-z0-9A-Z])+)$',
        ResetPasswordView.as_view(),
        name='account_reset_password'),
    

]
