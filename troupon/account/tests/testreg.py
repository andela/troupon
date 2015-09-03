from django.template.loader import render_to_string
from django.test import TestCase, Client

class RegViewTest(TestCase):
  def setUp(self):
    self.client_stub = Client()

  def test_view_reg_route(self):
    response = self.client_stub.get('/auth/signup/')
    self.assertEquals(response.status_code, 200)

  def test_view_reg_route(self):
    response = self.client_stub.get('/auth/signupreq/')
    csrf_client = Client(enforce_csrf_checks=True)
    self.assertEquals(response.status_code, 200)

  def test_view_reg_success_route(self):
    response = self.client_stub.get('/auth/confirm/')
    self.assertEquals(response.status_code, 200)


