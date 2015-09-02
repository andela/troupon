<<<<<<< HEAD

from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User


class UserSignInViewTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User(username='johndoe@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_view_get_auth_signin(self):
        """Test that user request for signin page binds to a view called
            the class name `UserSigninView`.
        """

        response = resolve('/auth/signin/')
        self.assertEquals(response.func.__name__, 'UserSigninView')

    def test_view_post_auth_signin(self):
        """Test that user post to signin route has a session
        """
        data = {'email': 'johndoe@gmail.com', 'password': '12345'}
        response = self.client.post('/auth/signin/', data)
        self.assertIn('deals', response.content)


=======
from django.test import TestCase, Client
>>>>>>> [#102569504] Feature: Forgot Password: test that a 'get' to ForgotPasswordView renders with email_form in context
class ForgotPasswordViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_get_status(self):
        response = self.client.get('/account/forgot_password/')
        self.assertEquals(response.status_code, 200)

    def test_get_context_has_email_form(self):
        response = self.client.get('/account/forgot_password/')
        self.assertContains(response.context, 'email_form')
