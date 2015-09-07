
from django.test import TestCase, Client
from django.contrib.auth.models import User
from account.views import ForgotPasswordView, ResetPasswordView

class UserSigninTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User(username='johndoe@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_route_get_auth_signin(self):
        response = self.client.get('/account/signin/')
        self.assertEquals(response.status_code, 200)

    def test_route_post_auth_signin(self):
        response = self.client.post('/account/signin/',
                                    dict(email='johndoe@gmail.com',
                                         password='12345'))
        self.assertEquals(response.status_code, 302)



class ForgotRecoverPasswordRoutesTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_forgot_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/')
        self.assertEqual(response.resolver_match.func.__name__, ForgotPasswordView.as_view().__name__)

    def test_reset_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/ajkzfYba9847DgJ7wbkwAaSbkTjUdawGG998qo3HG8qae83')
        self.assertEqual(response.resolver_match.func.__name__, ResetPasswordView.as_view().__name__)

class UserRegistrationViewTest(TestCase):
  '''
  Test class to user registration.
  '''
  def setUp(self):
    '''
    User sign's up with data.
    '''
    self.client_stub = Client()
    self.form_data = dict(username="andela",
                           password1="andela",
                           password2="andela",
                           email="andela@andela.com",
                           )

  def test_view_signup_route(self):
    '''
    User signup page is called.
    '''
    response = self.client_stub.get('/account/signup/')
    self.assertEquals(response.status_code, 200)

  def test_view_reg_route(self):
    '''
    User is redirected after signup data is validated.
    '''
    response = self.client_stub.post('/account/signup/', self.form_data)
    self.assertEquals(response.status_code, 302)

  def test_view_reg_success_route(self):
    '''
    User gets to view confirmation page after signup.
    '''

    response = self.client_stub.get('/account/confirm/')
    self.assertEquals(response.status_code, 200)