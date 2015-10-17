from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from deals.models import Deal, STATE_CHOICES
from django.template import Engine, RequestContext
import cloudinary


# Create your views here.
class HomePage(TemplateView):
    """class that handles display of the homepage"""

    template_name = "deals/index.html"
    context_var = {
        'show_subscribe': True,
        'show_search': True,                      
        'states': { 'choices': STATE_CHOICES,  'default': 25 },
        'popular_categories': [
            'Get Aways',
            'Fashion & Lifestyle',
            'Electronics',
            'Food',
            'Travel & Get Aways',
            'Fashion',
            'Electronics',
            'Food',
            'Travel',
            'Fashion',
            'Electronics',
            'Food',
            'Travel',
            'Fashion',
            'Electronics',
        ],
        'featured_deals': [
            {
                'pk': 1,
                'title': 'Fashion-holics Give Away',
                'advertiser': {
                    'name': 'DressToKill Boutique',
                    'address': 'Ikeja Shopping Mall, Ikeja.',
                },
                'price': '12800',
                'original_price': '25300',
                'slide_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_1600,h_700,c_fill/v1445000537/troupon0.jpg',
                'thumbnail_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_350,h_350,c_fill/v1445000537/troupon0.jpg',
            },
            {
                'pk': 2,
                'title': 'Fashion-holics Give Away',
                'advertiser': {
                    'name': 'DressToKill Boutique',
                    'address': 'No.23, Saint James Street, Ikeja Shopping Mall, Ikeja, Ikeja Shopping Mall, Ikeja, Lagos.',
                },
                'price': '12800',
                'original_price': '25300',
                'slide_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_1300,h_500,c_fill/v1445000562/troupon1.jpg',
                'thumbnail_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_350,h_350,c_fill/v1445000562/troupon1.jpg',
            },
            {
                'pk': 3,
                'title': 'Fashion-holics Give Away',
                'advertiser': {
                    'name': 'DressToKill Boutique',
                    'address': 'Ikeja Shopping Mall, Ikeja.',
                },
                'price': '12800',
                'original_price': '25300',
                'slide_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_1300,h_500,c_fill/v1445001720/troupon2.jpg',
                'thumbnail_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/w_350,h_350,c_fill/v1445001720/troupon2.jpg',
            },
            {
                'pk': 4,
                'title': 'Fashion-holics Give Away',
                'advertiser': {
                    'name': 'DressToKill Boutique',
                    'address': 'No.23, Saint James Street, Ikeja Shopping Mall, Ikeja, Ikeja Shopping Mall, Ikeja, Lagos.',
                },
                'price': '12800',
                'original_price': '25300',
                'slide_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/v1445000552/troupon3.jpg',
                'thumbnail_image_url': 'http://res.cloudinary.com/awiliuzo/image/upload/v1445000552/troupon3.jpg',
            },
        ],
    }

    def get(self, request):
        return render(request, self.template_name, self.context_var)


class DealView(View):
    """This handles request for each deal by id.
    """

    def get(self, *args, **kwargs):
        deal_id = self.kwargs.get('deal_id')  # get deal_id from request
        if not deal_id:
            deals = Deal.objects.all()
            engine = Engine.get_default()
            template = engine.get_template('deals/list.html')
            context = RequestContext(self.request, {'deals': deals})
            return HttpResponse(template.render(context))
        try:
            deal = Deal.objects.get(id=deal_id)
            deal = {'deal': deal}
        except Deal.DoesNotExist:
            raise Http404('Deal does not exist')

        # Replace template object compiled from template code
        # with an application template.
        # Use Engine.get_template(template_name)
        engine = Engine.get_default()
        template = engine.get_template('deals/detail.html')

        # set result in RequestContext
        context = RequestContext(self.request, deal)
        return HttpResponse(template.render(context))

    def post(self, request):
        """This handles creation of deals
        """
        try:
            deal = Deal(request.POST)
            response = self.upload(request.FILES, request.POST.get('title'))
            deal.photo_url = response.get('public_url')
            deal.save()
            return redirect('/deals/{0}/'.format(deal.id))
        except:
            return redirect('/deals/')

    def upload(self, file, title):
        return cloudinary.uploader.upload(
                file,
                public_id=title
            )
