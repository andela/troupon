from django.conf.urls import url

from userprofile import views 

urlpatterns = [
    url(r'^(?P<username>\w+)$', views.Userprofileview.as_view(), name = 'userprofile'),
    url(r'^merchant/$', views.MerchantView.as_view(), name ='merchant'),
    url(r'^verify/$', views.VerificationView.as_view(), name ='verify'),
]