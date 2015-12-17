from django.conf.urls import url

from views import UserProfileView, MerchantIndexView

urlpatterns = [

    url(r'^$',
        UserProfileView.as_view(),
        name='account'),

    url(r'^profile/$',
        UserProfileView.as_view(),
        name='account_profile'),

    url(r'^merchant/$',
        MerchantIndexView.as_view(),
        name='account_merchant'),

]
