from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.core.context_processors import csrf

class RegViewTest(TestCase):
  def setUp(self):
    self.client_stub = Client()
    self.form_data = dict(username="andela",
                           password1="andela",
                           password2="andela",
                           first_name="andela",
                           last_name="andela",
                           email="andela@andela.com",
                           )

  def test_view_reg_route(self):
    response = self.client_stub.get('/auth/signup/')
    self.assertEquals(response.status_code, 200)

  def test_view_reg_route(self):
    response = self.client_stub.post('/auth/signupreq/', self.form_data)
    self.assertEquals(response.status_code, 302)

  def test_view_reg_success_route(self):
    response = self.client_stub.get('/auth/confirm/')
    self.assertEquals(response.status_code, 200)


