from django.conf.urls import include, url
from deals import views

urlpatterns = [

    url(r'^auth/$',views.signup, name = 'signup'),
]
