from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
OWN_URL = reverse('user:self')


def create_user(**params):
    """create a user"""
    return get_user_model().objects.create_user(**params)


def sample_user():
    return {
        'email': 'user@email.com',
        'password': 'password123',
        'first_name': 'test',
        'last_name': 'name',
    }


class PublicUserTests(TestCase):
    """test publicly accessible api's"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successfully(self):
        """test creating an user with valid payload successfully"""
        payload = sample_user()

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_invalid_payload(self):
        """test creating a user with invalid payload fails"""

        payload = {
            'email': '',
            'password': ''
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """test creating user that already exists fails"""
        payload = sample_user()
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test creating user with password less than 5 characters fails """
        payload = {
            'email': 'user@email.com',
            'password': 'pass'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_successfully(self):
        """test creating a token when valid user logs in"""
        payload = sample_user()
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_for_invalid_user_details(self):
        """test creating token for invalid user credentials"""
        payload = {
            'email': 'user@email.com',
            'password': 'ppp'
        }
        user = sample_user()
        create_user(**user)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_for_non_existent_user(self):
        """test creating token for user that does not exist"""
        payload = sample_user()
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_required_fields(self):
        """test that required field must be passed to create token"""
        payload = {
            'email': 'user@email.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """test that authentication is required to access a profile"""
        res = self.client.get(OWN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTests(TestCase):
    """test api's that require authentication"""

    def setUp(self):
        user = sample_user()
        self.user = create_user(**user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_own_profile_successfully(self):
        """test that authenticated user is able to access their profile"""
        res = self.client.get(OWN_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        })

    def test_post_not_allowed_for_own_profile(self):
        """test that POST method is not allowed for retrieve profile url"""
        res = self.client.post(OWN_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_own_profile_update(self):
        """test updating profile for authenticated user"""
        payload = {
            'first_name': 'new',
            'password': 'new password'
        }

        res = self.client.patch(OWN_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
