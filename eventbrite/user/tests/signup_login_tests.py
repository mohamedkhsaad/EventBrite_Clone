from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ..serializers import *
from rest_framework.test import APITestCase


class AuthTokenSerializerTest(TestCase):
    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.username = 'testusername'
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


User = get_user_model()


class UserSerializerTest(APITestCase):
    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "test12345",
        }
        serializer = userSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        
