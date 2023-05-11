
from django.test import TestCase
from event.models import event
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

class EventModelTestCase(TestCase):
    def test_generate_unique_id(self):
        """
        Test that generate_unique_id() function generates unique IDs
        """
        # Create two events and ensure that their IDs are different
        event1 = event.objects.create(
            Title="Event 1", organizer="Organizer 1", user_id=1, 
            Summery="Summary 1", Description="Description 1", 
            type="Type", category_name="Category", 
            venue_name="Venue 1", ST_DATE="2023-06-01", END_DATE="2023-06-01", 
            ST_TIME="10:00:00", END_TIME="12:00:00", 
            online="True", CAPACITY=50, STATUS="Draft"
        )
        event2 = event.objects.create(
            Title="Event 2", organizer="Organizer 2", user_id=2, 
            Summery="Summary 2", Description="Description 2", 
            type="Type", category_name="Category", 
            venue_name="Venue 2", ST_DATE="2023-06-01", END_DATE="2023-06-01", 
            ST_TIME="14:00:00", END_TIME="16:00:00", 
            online="False", CAPACITY=100, STATUS="Live"
        )
        self.assertNotEqual(event1.ID, event2.ID)

    def test_create_event_with_invalid_date_format(self):
        # Create a new event with an invalid date format
        invalid_event = event(
            Title='Test Event',
            ST_DATE='2022/01/01',  # Invalid date format
            END_DATE='2022/01/02',
            ST_TIME=datetime.now().time(),
            END_TIME=datetime.now().time(),
            organizer='Test Organizer',
            Summery='Test Summery',
            Description='Test Description',
            type='Class, Training, or Workshop',
            category_name='Business & Professional',
            sub_Category='Test Sub-Category',
            venue_name='Test Venue',
            online='False',
            CAPACITY=50,
            STATUS='Draft',
        )
        # Assert that the event raises a validation error
        with self.assertRaises(ValidationError):
            invalid_event.full_clean()

# class EventCreateViewTestCase(APITestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = get_user_model().objects.create_user(
#             username='ismail',
#             email='ziad@gmail.com',
#             password='512002',)
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('event-create')
#     def test_create_event_with_empty_date(self):
#         data = {
#             'title': 'Test Event',
#             'description': 'A test event',
#             'start_time': '12:00',
#             'end_time': '13:00',
#             'online': True,
#             "ST_DATE": " ",
#             "END_DATE": "2023-05-10",
#             "ST_TIME": "05:00:00",
#             "END_TIME": "06:00:00",
#         }
#         response = self.client.post(self.url,data,format='multipart',follow=True)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('date', response.data)
#         self.assertEqual(response.data['date'][0], ' " " value has an invalid date format. It must be in YYYY-MM-DD format.')

# class TestEventCreateView(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = get_user_model().objects.create_user(
#             username='ismail',
#             email='ziad@gmail.com',
#             password='512002',)
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#     def test_create_event(self):
#         data = {
#             "Title": "kkkkkkkkkkkk",
#             "organizer": "ziad",
#             "Summery": "gggg",
#             "Description": "kkkk",
#             "type": "Attraction",
#             "category_name": "Science & Technology",
#             "sub_Category": "football",
#             "venue_name": "giza",
#             "ST_DATE": "2023-05-10",
#             "END_DATE": "2023-05-10",
#             "ST_TIME": "05:00:00",
#             "END_TIME": "06:00:00",
#             "online": "False",
#             "CAPACITY": "5000",
#             "STATUS": "Draft",
#         }
#         response = self.client.post(reverse('event-create'), data=data,follow=True)
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#         self.assertEqual(event.objects.count(), 1)
#         self.assertEqual(event.objects.first().Title, 'kkkkkkkkkkkk')
#         self.assertEqual(event.objects.first().user, self.user)

