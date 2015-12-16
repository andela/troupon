from django.test import TestCase

from general import SharedContextMiddleware
from mock import MagicMock


class SharedContextMiddlewareTestCase(TestCase):
    """
    Testcase for the SharedContextMiddleware class
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        """
        operations to run before every test
        """
        # instantiate a sample middleware:
        self.sc_middleware = SharedContextMiddleware()

        # setup a mock request object and
        # add a search key to the GET querystring parameters:
        self.request = MagicMock()
        self.request.GET = {'q': 'a_deal_search_key'}

        # setup a mock response object and
        # add a smaple context data:
        self.response = MagicMock()
        self.response.context_data = {
            'context_var_from_view': 'blah blah blah'
        }

    def test_that_middleware_updates_context_with_categories(self):
        """
        tests that the response context_data was updated with
        correct data for categories, cities, advertisers and search.
        """
        response = self.sc_middleware.process_template_response(
            self.request,
            self.response
        )
        # assert for cities data
        cities = response.context_data.get('cities')
        self.assertIsNotNone(cities)
        self.assertNotEqual(len(cities), 0)
        # assert for categories data
        categories = response.context_data.get('categories')
        self.assertIsNotNone(categories)
        self.assertNotEqual(len(categories), 0)
        # assert for advertisers data
        advertisers = response.context_data.get('advertisers')
        self.assertIsNotNone(advertisers)
        self.assertNotEqual(len(advertisers), 0)
        # assert for correct search query/options:
        search_options = response.context_data.get('search_options')
        self.assertIsNotNone(search_options)
        self.assertEqual(search_options.get('query'), 'a_deal_search_key')
        self.assertIsNotNone(search_options.get('default_city'))
        self.assertIsInstance(search_options.get('default_city'), int)

    def test_that_middleware_retains_previous_context_data(self):
        """
        tests that the response context_data set in the views is not
        discarded or overwritten in the middleware.
        """
        response = self.sc_middleware.process_template_response(
            self.request,
            self.response
        )
        # assert for previous data
        prev_context_data = response.context_data.get('context_var_from_view')
        self.assertIsNotNone(prev_context_data)
        self.assertEqual(prev_context_data, 'blah blah blah')
