# from django.test import TestCase, RequestFactory
# from django.core.urlresolvers import reverse

# from deals.baseviews import DealListBaseView
# from deals.models import Deal, STATE_CHOICES, EPOCH_CHOICES


# class DealListBaseViewTestCase(TestCase):
#     """ This testcase excercises the functions of the DealListBaseView
#         as isolated units.
#     """

#     # load the deal fixtures:
#     fixtures = ['test_data',]

#     def setUp(self):

#         # set the request factory
#         self.request_factory = RequestFactory()

#         # setup as an instance of the view:
#         self.base_view = DealListBaseView()

        
#     def test_renders_deal_list_to_str_correctly(self):
#         """ Tests that the DealListBaseView.rendered_deal_list method properly renders
#             a queryset of deals and returns it as a unicode string.
#         """
#         # prepare a request:
#         request = self.request_factory.get( "{}?dtf=4&pg=2".format(reverse('deals')) )

#         # render the view to string:
#         rendered_deal_list = self.base_view.render_deal_list(
#             request,
#             deals=Deal.objects.all(),
#             title="Latest Deals", 
#             description="Hot and sizzling deals",
#             zero_items_message = "Sorry, no deals found!",
#             num_page_items = 3,
#             pagination_base_url=reverse('deals')
#         )
#         print rendered_deal_list
#         # test the returned unicode str:
#         self.assertIsInstance(rendered_deal_list, unicode)
#         self.assertIn('Latest Deals', rendered_deal_list)
#         self.assertIn('Hot and sizzling deals', rendered_deal_list)
#         self.assertIn('value="-1" selected', rendered_deal_list)
#         self.assertIn('Showing 4 - 6 of 10 items', rendered_deal_list)
#         self.assertEqual(rendered_deal_list.count('grid-item'), 3)
