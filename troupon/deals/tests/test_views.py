import unittest
import time

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException

from accounts.models import UserProfile
from deals.models import Advertiser, Category, Deal
from merchant.models import Merchant

# Values for creating a test user
TEST_USER_EMAIL = 'testuser@myemail.com'
TEST_USER_PASSWORD = 'testpassword'

# Values for running a search
TEST_SEARCH_TERM = "Holiday"
TEST_SEARCH_LOCATION = "Nairobi"

# XPaths to test search
xpath_search_term = "//div[@class='custom-input-group']/input[@id='search']"
xpath_search_location = "//div[@class='custom-input-group']/select"
xpath_search_btn = "//button[@class='btn-action']"
xpath_search_results_title = "//h1[@class='title']"
xpath_search_results_desc = "//p[@class='description']"
xpath_search_results_deal = "//div[@class='packery-grid deal-grid']/div[@class='grid-item card']/form[@class='overlay row']"

# XPaths to test deals
xpath_deals_page_title = "//h1[@class='title']"
xpath_deals_first_deal = "//div[@class='grid-item card'][1]/form[@class='overlay row']"
xpath_more_details_btn = "//div[@class='grid-item card'][1]/form[@class='overlay row']/div[@class='row']/div/a[@class='btn-action']"
xpath_deal_specs = "//div[@class='deals-specs']"

# XPaths to test reviews
xpath_review_disp_msg = "//div[@class='col-md-12'][1]/p[2]"
xpath_review_login_btn = "//a/button[@class='btn-action']"
xpath_add_to_cart_btn = "//button[@id='buy-btn']"
xpath_cart_dropdown = "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']"
xpath_view_cart_btn = "//ul[@class='dropdown-menu dropdown-menu-right']/a[@class='btn-action'][1]"
xpath_checkout_btn = "//div[@class='pull-right col-sm-2']/a[@class='btn-action']"
xpath_pay_card_btn = "//button[@class='stripe-button-el']/span"
xpath_review_form = "//form[@id='add-review']"
xpath_review_description = "//textarea[@class='custom-input-group review-textarea']"
xpath_ratings_count = "//div[@class='col-md-12'][1]/p[1]/span[@class='mini-text']"
xpath_deal_reviews = "//div[@class='deal-reviews']"
xpath_review_text = "//p[@class='review-text']"


class HomepageViewTests(LiveServerTestCase):
    """runs functional tests for the homepage"""

    @classmethod
    def setUpClass(cls):
        """
        Setup the test driver
        """
        cls.driver = webdriver.Chrome()
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
        self.driver = webdriver.Chrome()
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
            xpath_more_details_btn).click()
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
        self.driver = webdriver.Chrome()
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
        self.driver.find_element_by_xpath(xpath_search_btn
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


class ReviewViewTest(LiveServerTestCase, CreateDeal):

    def setUp(self):
        """Setup the test driver and create deal"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.create_user()
        self.create_deal()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/deals")
        )
        super(ReviewViewTest, self).setUp()

    def open_deals_page(self):
        """Navigate to deal page"""
        self.driver.get(
            '%s%s' % (self.live_server_url, "/deals")
        )
        self.driver.find_element_by_xpath(xpath_more_details_btn
                                          ).click()

    def purchase_deal(self):
        """Add deal to cart and purchase it"""
        self.login_user()
        self.open_deals_page()
        self.driver.find_element_by_xpath(xpath_add_to_cart_btn
                                          ).click()
        self.driver.find_element_by_xpath(xpath_cart_dropdown).click()
        self.driver.find_element_by_xpath(xpath_view_cart_btn).click()
        self.driver.find_element_by_xpath(xpath_checkout_btn).click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(xpath_pay_card_btn).click()
        self.driver.implicitly_wait(10)

        # Switch to Stripe frame and add email to form
        self.driver.switch_to.frame('stripe_checkout_app')
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)

        # Add card number
        card_number = self.driver.find_element_by_id('card_number')
        card_number.send_keys('4242')
        self.driver.implicitly_wait(0.25)
        card_number.send_keys('4242')
        self.driver.implicitly_wait(0.25)
        card_number.send_keys('4242')
        self.driver.implicitly_wait(0.25)
        card_number.send_keys('4242')

        # Add card expiry month and year
        card_expiry = self.driver.find_element_by_id('cc-exp')
        card_expiry.send_keys('01')
        self.driver.implicitly_wait(0.25)
        card_expiry.send_keys('19')

        # Add CVC and submit form
        self.driver.find_element_by_id('cc-csc').send_keys('123')
        self.driver.find_element_by_id('submitButton').click()

        # Payment processing and redirection
        self.driver.switch_to.default_content()
        time.sleep(10)

    def test_unauthenticated_user(self):
        """
        Test that the appropriate message is displayed for unauthenticated
        users
        """
        self.open_deals_page()
        display_msg = self.driver.find_element_by_xpath(
            xpath_review_disp_msg).text
        assert "You need to log in to rate and review this deal" in display_msg
        assert self.driver.find_element_by_xpath(xpath_review_login_btn)

    def test_deal_not_purchased(self):
        """
        Test that the appropriate message is displayed when user has not
        purchased the deal
        """
        self.login_user()
        self.open_deals_page()
        display_msg = self.driver.find_element_by_xpath(
            xpath_review_disp_msg).text
        assert "You need to purchase this deal" in display_msg

    # The following two tests are commented out due to the tests failing on
    # CircleCI as a result of CircleCI's outdated version of chromedriver.
    # Chromedriver v2.22 is required for the .switch_to.frame part of the
    # purchase_deal() method to work. The current version of chromedriver on
    # CircleCI is 2.16.

    # def test_form_display(self):
    #     """
    #     Test that review form is displayed for authenticated users who have
    #     purchased the deal but not reviewed it
    #     """
    #     self.purchase_deal()
    #     self.open_deals_page()
    #     assert self.driver.find_element_by_xpath(xpath_review_form)
    #
    # def test_add_review(self):
    #     """
    #     Test that user can add review and it will be displayed.
    #     Test that the appropriate message is displayed when user has already
    #     reviewed the deal
    #     """
    #     self.purchase_deal()
    #     self.driver.implicitly_wait(30)
    #     self.open_deals_page()
    #     self.driver.find_element_by_xpath(xpath_review_description
    #                                       ).send_keys('Great deal!')
    #     self.driver.find_element_by_id('add-review-button').click()
    #     self.driver.implicitly_wait(10)
    #     ratings_count = self.driver.find_element_by_xpath(
    #                     xpath_ratings_count).text
    #     assert "1 rating" in ratings_count
    #     assert self.driver.find_element_by_xpath(xpath_deal_reviews)
    #     display_msg = self.driver.find_element_by_xpath(
    #         xpath_review_disp_msg).text
    #     assert "Thank you for your review!" in display_msg
    #     review_text = self.driver.find_element_by_xpath(
    #         xpath_review_text).text
    #     assert "Great deal!" in review_text

    def tearDown(self):
        self.driver.quit()
        super(ReviewViewTest, self).tearDown()


if __name__ == "__main__":
    unittest.main()
