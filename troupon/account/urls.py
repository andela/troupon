from django.conf.urls import url

from account import views

urlpatterns = [

    # pattern maps to view handling `GET` and `POST` requests to
    # /account
    url(r'^$',
        views.UserProfileView.as_view(),
        name='account'),

    # pattern maps to view handling `GET` and `POST` requests to
    # /account/profile/
    url(r'^profile/$',
        views.UserProfileView.as_view(),
        name='account_profile'),

    # pattern maps to view handling `GET` requests to
    # /account/merchant/
    url(r'^merchant/$',
        views.MerchantIndexView.as_view(),
        name='account_merchant'),

    # pattern maps to view handling `GET` and `POST` requests to
    # /account/merchant/register/
    url(r'^merchant/register/$',
        views.MerchantRegisterView.as_view(),
        name='account_merchant_register'),

    # pattern maps to view handling `GET` and `POST` requests to
    # /account/merchant/verify/
    url(r'^merchant/verify/$',
        views.MerchantVerifyVeiw.as_view(),
        name='account_merchant_verify'),

    # pattern maps to view handling `GET` requests to
    # /account/merchant/resendotp/
    url(r'^merchant/resendotp/$',
        views.MerchantResendOtpVeiw.as_view(),
        name='account_merchant_resendotp'),

    # pattern maps to view handling `GET` requests to
    # /account/merchant/confirm/
    url(r'^merchant/confirm/$',
        views.MerchantConfirmVeiw.as_view(),
        name='account_merchant_confirm'),

    # pattern maps to view handling `GET` and `POST` requests to
    # /account/change_password/
    url(r'^change_password/$',
        views.UserChangePasswordView.as_view(),
        name='account_change_password'),

]
