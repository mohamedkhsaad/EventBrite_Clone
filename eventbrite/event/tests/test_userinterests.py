from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock

from event.models import *
from event.serializers import *
from event.views import *


class UserInterestEventsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_user_interests(self):
        # Create a user interest
        user_interest = UserInterest.objects.create(
            user=self.user, category_name='Music', sub_Category='Rock')

        # Call the get_user_interests method
        view = UserInterestEventsAPIView()
        user_interests = view.get_user_interests(self.user)

        # Check that the user interest was retrieved
        self.assertEqual(len(user_interests), 1)
        self.assertEqual(user_interests[0].category_name, 'Music')
        self.assertEqual(user_interests[0].sub_Category, 'Rock')

    def test_get_events(self):
        # Create some events with matching categories and subcategories
        self.event1 = event.objects.create(
            ID=1,
            User_id=3,
            Title='Test Event',
            organizer=self.user,
            user=self.user,
            Summery='Test Event Summery',
            Description='Test Event Description',
            type='Test Event Type',
            category_name='Music',
            sub_Category='Rock',
            venue_name='Test Venue',
            ST_DATE='2023-05-15',
            END_DATE='2023-05-16',
            ST_TIME='10:00:00',
            END_TIME='18:00:00',
            online='True',
            CAPACITY=100,
            PASSWORD='test',
            STATUS='Live',
            image=None)
        self.event2 = event.objects.create(
            ID=2,
            User_id=3,
            Title='Test Event',
            organizer=self.user,
            user=self.user,
            Summery='Test Event Summery',
            Description='Test Event Description',
            type='Test Event Type',
            category_name='Music',
            sub_Category='Pop',
            venue_name='Test Venue',
            ST_DATE='2023-05-15',
            END_DATE='2023-05-16',
            ST_TIME='10:00:00',
            END_TIME='18:00:00',
            online='True',
            CAPACITY=100,
            PASSWORD='test',
            STATUS='Live',
            image=None)
        self.event3 = event.objects.create(
            ID=3,
            User_id=3,
            Title='Test Event',
            organizer=self.user,
            user=self.user,
            Summery='Test Event Summery',
            Description='Test Event Description',
            type='Test Event Type',
            category_name='Sports',
            sub_Category='Basketball',
            venue_name='Test Venue',
            ST_DATE='2023-05-15',
            END_DATE='2023-05-16',
            ST_TIME='10:00:00',
            END_TIME='18:00:00',
            online='True',
            CAPACITY=100,
            PASSWORD='test',
            STATUS='Live',
            image=None)
        # Create some user interests
        user_interest1 = UserInterest.objects.create(
            user=self.user, category_name='Music', sub_Category='Rock')
        user_interest2 = UserInterest.objects.create(
            user=self.user, category_name='Music', sub_Category='Pop')
        user_interest3 = UserInterest.objects.create(
            user=self.user, category_name='Sports', sub_Category='Basketball')

        # Call the get_events method
        view = UserInterestEventsAPIView()
        events = view.get_events([user_interest1, user_interest2])

        # Check that the correct events were retrieved
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].ID, '1')
        self.assertEqual(events[1].ID, '2')

    # def test_get(self):
    #     # Create some user interests
    #     user_interest1 = UserInterest.objects.create(
    #         user=self.user, category_name='Music', sub_Category='Rock')
    #     user_interest2 = UserInterest.objects.create(
    #         user=self.user, category_name='Music', sub_Category='Pop')
    #     user_interest3 = UserInterest.objects.create(
    #         user=self.user, category_name='Sports', sub_Category='Basketball')
    #     # Call the API endpoint
    #     url = reverse('user-interest-events')
    #     response = self.client.get(url)
    #     # Check that the response is successful and contains the correct data
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     serializer = eventSerializer([self.event1, self.event2], many=True)
    #     self.assertEqual(response.data, serializer.data)
