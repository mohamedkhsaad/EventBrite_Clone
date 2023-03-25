from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .serializers import *

class AuthTokenSerializerTest(TestCase):
    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.username='testusername'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            
        )
        self.serializer_data = {
            'email': self.email,
            'password': self.password
        }
    
    def test_auth_token_creation(self):
        serializer = AuthTokenSerializer(data=self.serializer_data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.create(user=self.user)
        self.assertEqual(serializer.validated_data['user'], self.user)
        self.assertEqual(serializer.validated_data['user'].auth_token, token)

