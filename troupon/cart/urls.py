from django.conf.urls import url
from cart.views import CheckoutView

urlpatterns = [
    # points to the checkout view handler
    url(r'^checkout/$',
        CheckoutView.as_view(),
        name='checkout'),
]
