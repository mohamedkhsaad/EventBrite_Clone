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
        self.event_sub_Category = 'pop'

        self.event1 = event.objects.create(
            ID="478", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="music", Category="test", sub_Category=self.event_sub_Category , venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")

        self.event2 = event.objects.create(
            ID="586", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="music", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")

    def test_get_events_by_sub_Category(self):
        """
        Test retrieving events by sub_Category.
        """
        url = reverse('event-list-by-sub_category',
                      kwargs={'event_sub_Category': self.event_sub_Category})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        event_data = response.data[0]
        serializer = eventSerializer(self.event1)
        self.assertEqual(event_data, serializer.data)

    def test_get_events_by_non_exist_sub_Category(self):
        """
        Test retrieving events by a sub_Category that does not exist.
        """
        nonexistent_sub_Category = 'nonexistent sub_Category'
        url = reverse('event-list-by-sub_category',
                      kwargs={'event_sub_Category': nonexistent_sub_Category})
        response = self.client.get(url)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
