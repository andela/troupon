from django.conf.urls import url
from conversations.views import MessagesView, MessageView, ComposeMessageView
from merchant.views import ManageDealsView, ManageDealView, TransactionsView,\
    TransactionView, CreateDealView, MerchantView

urlpatterns = [
    # pattern maps to view handling `POST` and `GET`
    #  requests to `/merchant/messages`
    url(
        r'^messages/$',
        MessagesView.as_view(),
        name='messages'
    ),

    # pattern maps to view handling `GET` requests
    # to `/merchant/messages/compose`
    url(
        r'^messages/compose/$',
        ComposeMessageView.as_view(),
        name='compose_message'
    ),

    # pattern maps to view handling `POST` and `GET`
    #  requests to `/merchant/messages/<m_id>`
    url(
        r'^message/(?P<m_id>[0-9]+)/$',
        MessageView.as_view(),
        name='message'
    ),

    # pattern maps to view handling `GET request to
    #  `/merchant/deals`
    url(
        r'^deals/$',
        ManageDealsView.as_view(), name='merchant_manage_deals',
    ),

    # pattern maps to view handling `GET` and `POST`
    # requests to `/merchant/deals/<slug>`
    url(
        r'^deals/(?P<deal_slug>[\w-]+)/$',
        ManageDealView.as_view(), name='merchant_manage_deal',
    ),

    # pattern maps to view handling `GET` request to
    #  `/merchant/transactions`
    url(
        r'^transactions/$',
        TransactionsView.as_view(), name='merchant_transactions',
    ),

    # pattern maps to view handling `GET` and `POST` to
    #  `/merchant/transactions/<transaction_id>`
    url(
        r'^transactions/(?P<transaction_id>[\d]+)/$',
        TransactionView.as_view(), name='merchant_transaction',
    ),

    # pattern maps to view handling `GET` and `POST` to
    #  `/merchant/deals/create`
    url(
        r'^deals/create/$',
        CreateDealView.as_view(), name='merchant_create_deal',
    ),

    # pattern maps to view handling `GET` to
    #  `/merchant/<merchant_slug>`
    url(
        r'^merchant/(?P<merchant_slug>[\w-]+)/$',
        MerchantView.as_view(), name='merchant_view',
    ),
]
