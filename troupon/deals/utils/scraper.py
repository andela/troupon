import os
from django.db.models import Sum
from django.contrib.auth.models import User
from troupon.settings.base import TROUPON_EMAIL
from django.template import Context, loader
from payment.models import Purchases
from authentication.emails import SendGrid


def send_periodic_emails():
    """
    Sends top 5 deals to registered users.

    Returns:
        Status code for sent email.

    """

    # get users who are not merchants
    users = User.objects.all()
    user_emails = []
    for user in users:
        user_emails.append(user.email)

    # Top 5 deals with highest number of buyers
    tops = Purchases.objects.all().annotate(
        qcount=Sum('quantity')).order_by('-qcount')[:5]

    deals = []
    for top in tops:
        deal = top.item

        deals.append(deal)

    # URL to Troupon
    troupon_url = os.getenv('TROUPON_HOME')

    # Compose the email
    message = SendGrid.compose(
        sender='Troupon <{}>'.format(TROUPON_EMAIL),
        subject="Trending deals in troupon",
        recipient=user_emails,
        text=None,
        html=loader.get_template(
            'deals/trending_deals.html'
        ).render(Context({
            'trending_deals': deals,
            'troupon_url': troupon_url
        }))
    )

    # send email
    response = SendGrid.send(message)
    return response
