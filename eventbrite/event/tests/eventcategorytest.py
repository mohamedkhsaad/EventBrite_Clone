from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model


class EventListtypeTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event_category = 'music'

        self.event1 = event.objects.create(
            ID="911", User_id="3", Title="Test Event", organizer="test",
            Description="test", type=self.event_category, Category= self.event_category , sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")
        
        self.event2 = event.objects.create(
            ID="91111", User_id="31", Title="Test Event", organizer="test",
            Description="test", type="food", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")

    def test_get_events_by_category(self):
        """
        Test retrieving events by category.
        """
        url = reverse('event-list-by-category', kwargs={'event_Category': self.event_category})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        event_data = response.data[0]
        serializer = eventSerializer(self.event1)
        self.assertEqual(event_data, serializer.data)

    def test_get_events_by_non_exist_category(self):
        """
        Test retrieving events by a category that does not exist.
        """
        nonexistent_category = 'nonexistent category'
        url = reverse('event-list-by-category', kwargs={'event_Category': nonexistent_category})
        response = self.client.get(url)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

