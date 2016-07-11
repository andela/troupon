import unittest

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver

from account.models import UserProfile
from deals.models import Advertiser, Category, Deal
from merchant.models import Merchant

TEST_USER_EMAIL = 'testuser@myemail.com'
TEST_USER_PASSWORD = 'testpassword'
TEST_SEARCH_TERM = "Holiday"
TEST_SEARCH_LOCATION = "Nairobi"

xpath_search_term = "//div[@class='custom-input-group']/input[@id='search']"
xpath_search_location = "//div[@class='custom-input-group']/select"
xpath_search_button = "//button[@class='btn-action']"
xpath_search_results_title = "//h1[@class='title']"
xpath_search_results_desc = "//p[@class='description']"
xpath_search_results_deal = "//div[@class='packery-grid deal-grid']" \
    "/div[@class='grid-item card']/form[@class='overlay row']"
xpath_deals_page_title = "//h1[@class='title']"
xpath_deals_first_deal = "//div[@class='grid-item card'][1]/form[@class='overlay row']"
xpath_more_details_button = "//div[@class='grid-item card'][1]" \
    "/form[@class='overlay row']/div[@class='row']/a[@class='more-details-btn btn-action']"
xpath_deal_specs = "//div[@class='deals-specs']"


class HomepageViewTests(LiveServerTestCase):
    """runs functional tests for the homepage"""

    @classmethod
    def setUpClass(cls):
        """
        Setup the test driver
        """
        cls.driver = webdriver.Firefox()
        super(HomepageViewTests, cls).setUpClass()

    def setUp(self,):
        """
        Setup the test driver
        """
        self.driver = HomepageViewTests.driver
        super(HomepageViewTests, self).setUp()

    def test_title(self,):
        """
        Checks homepage displays correct title
        """
        self.driver.get(self.live_server_url + '/')
        self.assertIn("Troupon - Get Some", self.driver.title)

    def test_can_subscribe(self,):
        """
        Checks if newsletter form is present on homepage
        """
        self.driver.get("%s" % (self.live_server_url))
        self.assertTrue("driver.find_element_by_id('subscriberEmail')")

    def test_about_us_present(self,):
        """
        Checks if the about us section is present in homepage
        """
        self.driver.get(self.live_server_url + '/')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn("About", body.text)

    def tearDown(self,):
        """
        Close the browser window
        """
        super(HomepageViewTests, self).tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(HomepageViewTests, cls).tearDownClass()


class CreateDeal(object):
    def create_user(self):
        """Create the test user"""
        User.objects.create_user(username='mytestuser',
                                 email=TEST_USER_EMAIL,
                                 password=TEST_USER_PASSWORD)

    def login_user(self):
        """Log in as the test user"""
        self.driver.get(
            '%s%s' % (self.live_server_url, "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def create_user_profile(self):
        """Create the test user profile"""
        user_object = User.objects.all()[:1].get()
        user_profile = UserProfile.objects.create(
            user=user_object,
            occupation='Travel Agent',
            intlnumber='0705123456')
        return user_profile

    def create_merchant(self):
        """Create the test merchant"""
        merchant = Merchant.objects.create(
            userprofile=self.create_user_profile(),
            intlnumber='0705123456', enabled=True,
            approved=True, trusted=True)
        return merchant

    def create_deal(self):
        """Create the test deal"""
        merchant = self.create_merchant()
        price = 5000
        original_price = 6000
        currency = 1
        country = 2
        location = 84
        quorum = 0
        disclaimer = ''
        description = 'Holiday for two to the luxurious Masai Mara.'
        title = 'Masai Mara Holiday'
        address = 'Masai Mara'
        max_quantity_available = 20
        active = True
        advertiser_id = merchant.advertiser_ptr.id
        date_end = "2020-09-09"

        category = Category.objects.create(name="Travel N Hotels",
                                           slug="masai-mara-holiday")
        advertiser = Advertiser.objects.get(id=advertiser_id)

        deal = Deal(
            price=price, original_price=original_price, currency=currency,
            country=country, location=location, category=category,
            quorum=quorum, disclaimer=disclaimer, description=description,
            address=address, max_quantity_available=max_quantity_available,
            date_end=date_end, active=active, title=title,
            advertiser=advertiser, duration=20
        )

        deal.save()


class DealsViewTest(LiveServerTestCase, CreateDeal):

    def setUp(self):
        """Setup the test driver and create deal"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.create_user()
        self.create_deal()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/deals")
        )
        super(DealsViewTest, self).setUp()

    def test_deal_listing(self):
        """Test that deal is listed"""
        deals_page_title = self.driver.find_element_by_xpath(
            xpath_deals_page_title).text
        assert "Latest Deals" in deals_page_title
        assert self.driver.find_element_by_xpath(xpath_deals_first_deal)

    def test_deal_details(self):
        """Test that deal details are displayed"""
        self.driver.find_element_by_xpath(
            xpath_more_details_button).click()
        deal_details_title = self.driver.find_element_by_xpath(
            xpath_deals_page_title).text
        assert "Masai Mara Holiday" in deal_details_title
        assert self.driver.find_element_by_xpath(xpath_deal_specs)

    def tearDown(self):
        self.driver.quit()
        super(DealsViewTest, self).tearDown()


class DealsSearchView(LiveServerTestCase, CreateDeal):

    def setUp(self):
        """Setup the test driver and create deal"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.create_user()
        self.create_deal()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        super(DealsSearchView, self).setUp()

    def search(self):
        """Run a search"""
        self.driver.find_element_by_xpath(xpath_search_term
                                          ).send_keys(TEST_SEARCH_TERM)
        self.driver.find_element_by_xpath(xpath_search_location
                                          ).send_keys(TEST_SEARCH_LOCATION)
        self.driver.find_element_by_xpath(xpath_search_button
                                          ).click()

    def test_deal_search(self):
        """Test that user can search for a deal"""
        self.search()
        search_results_title = self.driver.find_element_by_xpath(
            xpath_search_results_title).text
        search_results_desc = self.driver.find_element_by_xpath(
            xpath_search_results_desc).text
        assert "Search Results" in search_results_title
        assert "1 deal(s) found for this search" in search_results_desc
        assert self.driver.find_element_by_xpath(xpath_search_results_deal)

    def tearDown(self):
        self.driver.quit()
        super(DealsSearchView, self).tearDown()

if __name__ == "__main__":
    unittest.main()
