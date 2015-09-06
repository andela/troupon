from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.core.context_processors import csrf

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
                           first_name="andela",
                           last_name="andela",
                           email="andela@andela.com",
                           )

  def test_view_reg_route(self):
    '''
    User signup page is called.
    '''
    response = self.client_stub.get('/account/signup/')
    self.assertEquals(response.status_code, 200)

  def test_view_reg_route(self):
    '''
    User is redirected after signup data is validated.
    '''
    response = self.client_stub.post('/account/signuprequest/', self.form_data)
    self.assertEquals(response.status_code, 302)

  def test_view_reg_success_route(self):
    '''
    User gets to view confirmation page after signup.
    '''

    response = self.client_stub.get('/account/confirm/')
    self.assertEquals(response.status_code, 200)


