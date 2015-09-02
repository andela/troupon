from django.test import TestCase, Client


class ForgotPasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_route_forgot_password(self):
        response = self.client.get('/auth/forgot_password/')
        self.assertEquals(response.status_code, 200)
