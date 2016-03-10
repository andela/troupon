"""Imports statements."""
from django.conf.urls import url
from cart.views import CheckoutView, AddToCartView, ClearCartView, \
    RemoveItemView

urlpatterns = [
    # points to the checkout view handler
    url(r'^checkout/$',
        CheckoutView.as_view(),
        name='checkout'),
    # points to add to cart view which
    # adds item to cart and redirects back
    # to deals page
    url(r'^view/$',
        AddToCartView.as_view(),
        name='view'),
    # points to the clear cart view which
    # removes everything from thr cart and
    # redirects back to deals page
    url(r'^clear/$',
        ClearCartView.as_view(),
        name='clear'),
    # points to the remove item view
    # which removes one item from the
    # cart
    url(r'^remove/$',
        RemoveItemView.as_view(),
        name='remove')
]
