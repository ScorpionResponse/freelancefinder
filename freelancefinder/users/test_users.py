from django.test import TestCase

from authtools.models import User
import pytest


class LoginTests(TestCase):
    """
    Tests related to login success/failure
    """

    def setUp(self):
        User.objects.create_user(email='test1@example.com', password='test1')

    def test_login(self):
        """Test that logging in as a user works properly"""
        self.client.login(username='test1@example.com', password='test1')
        response = self.client.get('/')
        assert str(response.context['user']).endswith('<test1@example.com>')
        self.assertIn("AUTH:YES", response.content.decode('utf-8'),
                      "Proper login message not present.")

    def test_failed_login(self):
        """Test that logging in with an incorrect password fails"""
        self.client.login(username='test1@example.com', password='fail')
        response = self.client.get('/')
        assert not str(response.context['user']).endswith('<test1@example.com>')
        self.assertEqual(str(response.context['user']), 'AnonymousUser',
                         "Since the login failed, should still be anonymous, but are not")

    @pytest.mark.skip(reason="login form not created yet")
    def test_failed_login_in_form(self):
        """
        Test that logging in with an incorrect password generates an error on
        the page
        """
        data = {'username': 'test1', 'password': 'fail'}
        response = self.client.post('/accounts/login', data)
        self.assertFormError(response, 'form', None,
                             u'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        assert not str(response.context['user']).endswith('<test1@example.com>')
        self.assertEqual(str(response.context['user']), 'AnonymousUser',
                         "Since the login failed, should still be anonymous, but are not")

    def tearDown(self):
        user = User.objects.get(email='test1@example.com')
        user.delete()
