import os
import uuid

from django.conf import settings
from django.views.generic import View
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
import qrcode
from weasyprint import HTML, CSS

from deals.models import Deal
from tickets.models import Ticket


# Create your views here.
class DownloadView(View):
    """
    This class generates a ticket for users virtual purchases
    """
    def get(self, request, *args, **kwargs):
        """
        Handles get request to the 'download_ticket' named route

        Returns:
            A PDF response containing the ticket
        """
        user = request.user
        deal_id = kwargs['deal_id']
        deal = Deal.objects.get(pk=deal_id)
        quantity = int(request.GET.get('qty', 1))
        price = quantity * deal.price
        qr_img_url, unique_id = self.generate_unique_code(deal, user)
        logo_url = deal.advertiser.logo_image_url()

        # add ticket to database
        ticket = Ticket(
            user=user, item=deal, quantity=quantity,
            advertiser=deal.advertiser, ticket_id=unique_id
        )
        ticket.save()

        context = {
            'deal': deal,
            'logo_url': logo_url,
            'qr_img_url': qr_img_url,
            'issue_date': ticket.date_created,
            'quantity': quantity,
            'price': price,
            'user': user
        }
        html_template = get_template('tickets/ticket.html')
        rendered_html = html_template.render(
            RequestContext(request, context)).encode(encoding="UTF-8")
        styles = [
            CSS(string='.well-print { background-color: grey !important }'),
            CSS(
                settings.STATIC_ROOT + '/bootstrap/dist/css/bootstrap.min.css'
            ),
            CSS(settings.STATIC_ROOT + '/css/base_styles.css'),
        ]
        pdf_file = HTML(
            string=rendered_html,
            base_url=request.build_absolute_uri()) \
            .write_pdf(stylesheets=styles)

        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename=%s' % deal.slug
        return http_response

    def generate_unique_code(self, deal, user):
        """
        Generates Tickets for virtual deals

        Arguments:
            deal -- object representing the deal being purchased
            user -- object representing customer

        Returns:
            filename -- name of the file where QR code is stored
            id       -- unique ID generated for this transaction
        """
        # Converts utf8 to ascii strings because that is what UUID works with
        merchant_name = deal.advertiser.name.encode("utf8")
        deal_name = deal.advertiser.name.encode("utf8")
        username = user.username.encode("utf8")

        # Generates a unique code with python's UUID library
        # and embed in qrcode
        id = uuid.uuid5(
            uuid.NAMESPACE_DNS, merchant_name + deal_name + username
        )
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(id)
        qr.make(fit=True)

        img = qr.make_image()
        filename = 'img/%s.png' % id
        file_path = 'static/%s' % filename
        img.save(file_path)
        return filename, id
