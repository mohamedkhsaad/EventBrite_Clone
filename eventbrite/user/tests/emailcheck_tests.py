from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class EmailCheckViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'username' : 'testusername'
        }
        
        self.user = self.user_model.objects.create_user(**self.user_data)
        self.url = reverse('email-check', kwargs={'email': self.user_data['email']}) + '/'

    def test_email_check_returns_true_for_existing_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'email_exists': True})

    def test_email_check_returns_false_for_non_existing_user(self):
        non_existing_email = 'nonexistinguser@example.com'
        url = reverse('email-check', kwargs={'email': non_existing_email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'email_exists': False})
