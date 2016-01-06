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

    url(r'^change_password/$',
        views.UserChangePasswordView.as_view(),
        name='account_change_password'),

]
