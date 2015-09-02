from django.template.loader import render_to_string
from django.test import TestCase, Client

class RegViewTest(TestCase):
  def setUp(self):
    self.client_stub = Client()

  def test_view_reg_route(self):
    response = self.client_stub.get('/auth/signin/')
    self.assertEquals(response.status_code, 200)

