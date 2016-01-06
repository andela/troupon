from django.conf.urls import url

from account import views

urlpatterns = [

    url(r'^$',
        views.UserProfileView.as_view(),
        name='account'),

    url(r'^profile/$',
        views.UserProfileView.as_view(),
        name='account_profile'),

    url(r'^merchant/$',
        views.MerchantIndexView.as_view(),
        name='account_merchant'),

    url(r'^merchant/register/$',
        views.MerchantRegisterView.as_view(),
        name='account_merchant_register'),

    url(r'^merchant/verify/$',
        views.MerchantVerifyVeiw.as_view(),
        name='account_merchant_verify'),

    url(r'^merchant/confirm/$',
        views.MerchantConfirmVeiw.as_view(),
        name='account_merchant_confirm'),

    url(r'^change_password/$',
        views.UserChangePasswordView.as_view(),
        name='account_change_password'),

]
