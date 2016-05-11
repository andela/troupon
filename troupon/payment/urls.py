from django.conf.urls import url
from payment.views import PaymentProcessView, PaymentStatusView


urlpatterns = [
    url(r'^process/$',
        PaymentProcessView.as_view(),
        name='process_payment'),
    url(r'^status/$',
        PaymentStatusView.as_view(),
        name='payment_status'),
]
