from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from user.models import CustomToken
from ..serializers import *
from rest_framework.test import APITestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework import status
# from ..serializers import AuthTokenSerializer
from ..views import CustomTokenLoginView


User = get_user_model()

class CustomTokenLoginViewTest(TestCase):
    def setUp(self):
        self.username='testusername'
        self.email = 'testuser@example.com'
        self.password = 'TestPassword12^&'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.factory = APIRequestFactory()

    def test_custom_token_login(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        request = self.factory.post('/custom-token-login/', data=data)
        view = CustomTokenLoginView.as_view()
        response = view(request)

        # Assertions for the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)

        # Additional assertions if needed
        # ...

class AuthTokenSerializerTest(TestCase):
    def test_validate_credentials(self):
        username='testusername'
        email = 'testuser@example.com'
        password = 'TestPassword12^&'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        data = {
            "username":username,
            "email": email,
            "password": password,
        }
        serializer = AuthTokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        # Assertions for the validated data
        self.assertEqual(validated_data['email'], email)
        self.assertEqual(validated_data['password'], password)


User = get_user_model()


class UserSerializerTest(APITestCase):
    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Test123^&45",
        }
        serializer = userSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        
