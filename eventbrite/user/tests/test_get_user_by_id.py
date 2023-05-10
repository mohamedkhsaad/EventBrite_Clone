import json
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from rest_framework import status
from ..views import get_user_by_id

class GetUserByIdTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_user_by_id_existing_user(self):
        user_id = 12 # The ID of an existing user in the database
        request = self.factory.get('/users/{}/'.format(user_id))
        response = get_user_by_id(request, user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add more assertions to check the response data

    def test_get_user_by_id_nonexistent_user(self):
        user_id = 999  # An ID that doesn't exist in the database
        request = self.factory.get('/users/{}/'.format(user_id))
        response = get_user_by_id(request, user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {'user_exists': False})
        # Add more assertions if necessary

    # Add more test cases if needed
