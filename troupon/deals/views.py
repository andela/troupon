import cloudinary

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.template.defaultfilters import slugify
from django.db.models import Avg
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet
from datetime import date

from models import Category, Deal, Advertiser, ALL_LOCATIONS, Review
from payment.models import Purchases
from forms import ReviewForm
from baseviews import DealListBaseView
from geoip import geolite2
from django.http import JsonResponse


class HomePageView(DealListBaseView):
    """ View class that handles display of the homepage.
        Overrides the base get method, but still uses
        the base render_deal_list method to get the
        rendered latest deals listing.
    """

    def get(self, request, *args, **kwargs):
        # get the popular categories:
        popular_categories = Category.objects.all()[:12]

        # get the featured deals:
        featured_deals = Deal.objects.filter(featured=True).order_by('pk')[:5]

        # get the latest deals i.e. sorted by latest date:
        latest_deals = Deal.objects.filter(active=True)\
                                   .order_by('date_last_modified')
        list_title = "Latest Deals"
        list_description = "Checkout the hottest new deals from all your favourite brands:"

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            queryset=latest_deals,
            title=list_title,
            description=list_description,
            pagination_base_url=reverse('deals')
        )

        # return a JSON response if request is javascript ajax
        if request.is_ajax():
            return JsonResponse({'html': rendered_deal_list})

        context = {
            'popular_categories': popular_categories,
            'featured_deals': featured_deals,
            'rendered_deal_list': rendered_deal_list
        }
        context.update(csrf(request))
        return TemplateResponse(request, 'deals/index.html', context)


class DealsView(DealListBaseView):
    """ View class that handles display of the deals page.
        Simply configures the options and makes use of the base methods
        to render return latest deals listing.
    """
    queryset = Deal.objects.filter(active=True).order_by('date_last_modified')
    title = "Latest Deals"
    description = "See all the hottest new deals from all your favourite brands:"


class FilteredDealsView(DealListBaseView):
    """ Displays deals filtered by category, city or merchant.
        Works with routes of the form: '/deals/:filter_type/:filter_slug/'
    """
    category_title_format = "{} deals"
    city_title_format = "Deals in {}"
    advertiser_title_format = "Deals from {}"

    category_description_format = "See all the hot new {} deals!"
    city_description_format = "See all the hot new deals in {}!"
    advertiser_description_format = "See all the hot new from {}!"

    def get_queryset(self):
        """ returns the default deals queryset.
            override this method to return custom querysets.
        """
        filter_type = self.kwargs.get('filter_type')
        filter_slug = self.kwargs.get('filter_slug')
        queryset = self.queryset

        print filter_slug

        if filter_type == 'category':
            category = get_object_or_404(Category, slug=filter_slug)
            self.title = self.category_title_format\
                             .format(category.name)
            self.description = self.category_description_format\
                                   .format(category.name)
            queryset = queryset.filter(category=category)

        elif filter_type == 'merchant':
            advertiser = get_object_or_404(Advertiser, slug=filter_slug)
            self.title = self.advertiser_title_format\
                             .format(advertiser.name)
            self.description = self.advertiser_description_format\
                                   .format(advertiser.name)
            queryset = queryset.filter(advertiser=advertiser)

        elif filter_type == 'city':
            try:
                location = [location for location in ALL_LOCATIONS
                            if slugify(location[1]) == filter_slug][0]
            except:
                raise Http404('Not found')

            self.title = self.city_title_format\
                             .format(location[1])
            self.description = self.city_description_format\
                                   .format(location[1])
            queryset = queryset.filter(location=location[0])
        else:
            raise SuspiciousOperation('Invalid request')

        return queryset


class DealHaystackSearchView(View):
    """
    Haystack search class for auto complete.
    """
    template_name = 'deals/ajax_search.html'

    def get(self, request):
        deals = SearchQuerySet().autocomplete(
            content_auto=request.GET.get('q', '')
        )
        return TemplateResponse(request, self.template_name, {'deals': deals})


class DealSearchCityView(DealListBaseView):

    """ class to search for deals via title and locations"""
    pass

    def get(self, request, *args, **kwargs):
        value = request.GET.get('q', '')
        cityquery = int(request.GET.get('city', '25'))
        # get the deal results:
        deals = Deal.objects.filter(title__icontains=value)\
                            .filter(location__icontains=cityquery)

        # get the rendered list of deals
        rendered_deal_list = self.render_deal_list(
            request,
            queryset=deals,
            title='Search Results',
            zero_items_message='Your search - {} - in {} \
            did not match any deals.'
            .format(value, ALL_LOCATIONS[cityquery - 1][1]),
            description='{} deal(s) found for this search.'.format(len(deals))
        )
        context = {
            'rendered_deal_list': rendered_deal_list
        }
        context.update(csrf(request))
        return TemplateResponse(request, 'deals/searchresult.html', context)


class DealSlugView(View):
    """ Respond to routes to deal url using slug
    """

    def get(self, request, *args, **kwargs):
        deal_slug = self.kwargs.get('deal_slug')
        try:
            deal = Deal.objects.filter(slug=deal_slug)
            if len(deal) > 1:
                deal = deal[0]
            else:
                deal = deal[0]
        except (Deal.DoesNotExist, AttributeError):
            raise Http404('Deal with this slug not found!')

        reviews = Review.objects.filter(deal=deal)

        # Getting the average_rating rounded to the nearest integer
        average_rating_dict = Review.objects.filter(
                              deal=deal).aggregate(Avg('rating'))
        average_rating = average_rating_dict['rating__avg']
        if average_rating is None:
            average_rating = 0
        average_rating_rounded = round(average_rating)

        # Getting the number of reviews for each deal
        review_number = Review.objects.filter(deal=deal).count()
        if review_number == 1:
            review_count = str(review_number) + " rating"
        else:
            review_count = str(review_number) + " ratings"

        # Display the average rating in stars
        ratings_full = list(range(1, int(average_rating_rounded) + 1))
        ratings_empty = list(range(1, 6 - len(ratings_full)))
        if len(ratings_empty) == 5:
            ratings_msg = "No ratings yet!"
        else:
            ratings_msg = review_count

        display_form = False
        display_msg = ""

        if request.user.is_authenticated():
            user = self.request.user

            # Getting the deals purchased by the current user
            transactions = Purchases.objects.filter(user=user)
            purchased_deals = [transaction.item.id for transaction in transactions]

            # Getting the deals already reviewed by the current user
            user_reviews = Review.objects.filter(author=user)
            already_reviewed = [review.deal.id for review in user_reviews]

            # Check when to display form
            if deal.id in purchased_deals:
                if deal.id not in already_reviewed:
                    display_form = True
                else:
                    display_msg = "Thank you for your review! It'll go a long \
                                    way in ensuring we provide only the very \
                                    best deals."
            else:
                display_msg = "You need to purchase this deal to rate or \
                              review it."
        else:
            display_msg = "You need to log in to rate and review this deal."

        context = {'deal': deal,
                   'reviews': reviews,
                   'average_rating_rounded': average_rating_rounded,
                   'ratings_full': ratings_full,
                   'ratings_empty': ratings_empty,
                   'ratings_msg': ratings_msg,
                   'display_form': display_form,
                   'display_msg': display_msg
                   }

        return TemplateResponse(request, 'deals/detail.html', context)


class ReviewView(View):

    def post(self, request):
        """ View to handle creation of reviews"""
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.description = request.POST.get('description')
            review.rating = request.POST.get('rating')
            review.author = self.request.user
            review.date_created = date.today()
            deal_id = request.POST.get('deal_id')
            review.deal = Deal.objects.get(id=deal_id)
            deal_slug = review.deal.slug
            review.save()
            return HttpResponseRedirect(reverse('deal-with-slug',
                                        kwargs={'deal_slug': deal_slug}))
        else:
            print "The form cannot be empty."

        context = {'review_form': review_form}
        return TemplateResponse(request, 'deals/detail.html', context)
