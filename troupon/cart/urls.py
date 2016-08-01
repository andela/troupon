"""Imports statements."""
from django.conf.urls import url
from cart.views import CheckoutView, AddToCartView, ClearCartView, \
    RemoveItemView, ViewCartView, AddShippingDetails

urlpatterns = [
    # points to the checkout view handler
    url(r'^checkout/$',
        CheckoutView.as_view(),
        name='checkout'),
    # points to add to cart view which
    # adds item to cart and redirects back
    # to deals page
    url(r'^add/$',
        AddToCartView.as_view(),
        name='add'),
    # points to view cart view which
    # renders a template showing all items in cart
    url(r'^view/$',
        ViewCartView.as_view(),
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
        name='remove'),
    # points to view to add shipping details
    url(r'^shipping/$',
        AddShippingDetails.as_view(), name='proceed_checkout',
    ),
]
