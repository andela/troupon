from django.conf.urls import url
from cart.views import CheckoutView

urlpatterns = [
    url(r'^checkout/$',
        CheckoutView.as_view(),
        name='checkout'),
]
