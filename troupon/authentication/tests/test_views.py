from django.test import TestCase, Client, LiveServerTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from selenium import webdriver


class UserLoginViewTestCase(TestCase):
    """
    Test that post and get requests to login routes is successful
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_view_get_auth_login(self):
        """
        Test that user request for login page binds to a view called
        the class name `UserLoginView`.
        """
        response = resolve('/login/')
        self.assertEquals(response.func.__name__, 'UserLoginView')

    def test_view_post_auth_login(self):
        """
        Test that user post to login route has a session
        """
        data = {'username': 'johndoe@gmail.com', 'password': '12345'}
        response = self.client.post('/login/', data)
        self.assertEquals(response.status_code, 302)


class UserLogoutViewTestCase(TestCase):
    """
    Test that user can logout of session.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_route_get_auth_logout(self):
        self.client.post('/login',
                         dict(username='johndoe@gmail.com',
                              password='12345'))
        response = self.client.get('/logout/')
        self.assertIsNone(response.context)
        self.assertEquals(response.status_code, 302)


class UserRegisterViewTestCase(LiveServerTestCase):
    """
    End to End testing of user registration and login pages
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup the test driver
        """
        cls.driver = webdriver.PhantomJS()
        super(UserRegisterViewTestCase, cls).setUpClass()

    def setUp(self,):
        """
        Setup the test driver
        """
        User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin'
        )
        self.driver = UserRegisterViewTestCase.driver
        super(UserRegisterViewTestCase, self).setUp()

        # socket.setdefaulttimeout(10)

    def test_login_user(self,):
        """
        Checks if a user can sign in
        """
        url = "%s%s" % (self.live_server_url, reverse('login'))
        self.driver.get(url)
        # input login details and submit
        self.driver.find_element_by_id("email").send_keys('admin')
        self.driver.find_element_by_id("password").send_keys('admin')
        self.driver.find_element_by_id("loginBtn").click()

        # assert user is signed in
        self.driver.implicitly_wait(20)
        self.assertIn("Logged in as:", self.driver.page_source)

    def test_user_can_register(self,):
        """
        Checks if user can register on login page
        """
        url = "%s%s" % (self.live_server_url, reverse('login'))
        self.driver.get(url)
        self.driver.find_element_by_id("user_register_link").click()
        self.assertIn("Log in", self.driver.page_source)

    def tearDown(self,):
        """
        Close the browser window
        """
        super(UserRegisterViewTestCase, self).tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(UserRegisterViewTestCase, cls).tearDownClass()


class ActivateAccountViewTestCase(TestCase):
    """
    Test that user acount is activated.
    """
    def setUp(self):
        self.client_stub = Client()
        self.form_data = dict(
            username="andela",
            password1="andela",
            password2="andela",
            email="samuel.james@andela.com",
        )

    def test_activation_mail_sent(self):

        response = self.client_stub.post('/register/', self.form_data)
        self.assertEqual(302, response.status_code)


class ForgotPasswordViewTestCase(TestCase):
    """
    Test that can recover account through mail.
    """
    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.user = User.objects.create_user(
            'AwiliUzo', 'awillionaire@gmail.com', 'Young1491')
        self.user.first_name = 'Uzo'
        self.user.last_name = 'Awili'
        self.user.save()

    def test_get_returns_200(self):
        response = self.client.get('/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_post_returns_200(self):
        response = self.client.get('/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_recovery_email_sent_for_registered_user(self):
        response = self.client.post(
            '/recovery/', {"email": self.user.email}
        )
        self.assertIn('registered_user', response.context)
        self.assertIn('recovery_mail_status', response.context)

    def test_recovery_email_not_sent_for_unregistered_user(self):
        response = self.client.post(
            '/recovery/', {"email": "unregistereduser@andela.com"})
        self.assertNotIn('registered_user', response.context)
        self.assertNotIn('recovery_mail_status', response.context)
