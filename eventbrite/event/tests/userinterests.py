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
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_user_interests(self):
        # Create a user interest
        user_interest = UserInterest.objects.create(user=self.user, category_name='Music', sub_Category='Rock')
        
        # Call the get_user_interests method
        view = UserInterestEventsAPIView()
        user_interests = view.get_user_interests(self.user)

        # Check that the user interest was retrieved
        self.assertEqual(len(user_interests), 1)
        self.assertEqual(user_interests[0].category_name, 'Music')
        self.assertEqual(user_interests[0].sub_Category, 'Rock')

    def test_get_events(self):
        # Create some events with matching categories and subcategories
        event1 = event.objects.create(ID="911", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="event", category_name='Music', sub_Category='Rock', venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test"
        )
        event2 = event.objects.create(ID="911", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="event", category_name='Music', sub_Category='Pop', venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test"
        )
        event3 = event.objects.create(ID="911", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="event", category_name='Sports', sub_Category='Basketball', venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test"
        )
        # Create some user interests
        user_interest1 = UserInterest.objects.create(user=self.user, category_name='Music', sub_Category='Rock')
        user_interest2 = UserInterest.objects.create(user=self.user, category_name='Music', sub_Category='Pop')
        user_interest3 = UserInterest.objects.create(user=self.user, category_name='Sports', sub_Category='Basketball')

        # Call the get_events method
        view = UserInterestEventsAPIView()
        events = view.get_events([user_interest1, user_interest2])

        # Check that the correct events were retrieved
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].name, 'Event 1')
        self.assertEqual(events[1].name, 'Event 2')

    def test_get(self):
        # Create some events with matching categories and subcategories
        event1 = event.objects.create(name='Event 1', category_name='Music', sub_Category='Rock')
        event2 = event.objects.create(name='Event 2', category_name='Music', sub_Category='Pop')
        event3 = event.objects.create(name='Event 3', category_name='Sports', sub_Category='Basketball')

        # Create some user interests
        user_interest1 = UserInterest.objects.create(user=self.user, category_name='Music', sub_Category='Rock')
        user_interest2 = UserInterest.objects.create(user=self.user, category_name='Music', sub_Category='Pop')
        user_interest3 = UserInterest.objects.create(user=self.user, category_name='Sports', sub_Category='Basketball')

        # Call the API endpoint
        url = reverse('user-interest-events')
        response = self.client.get(url)

        # Check that the response is successful and contains the correct data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = eventSerializer([event1, event2], many=True)
        self.assertEqual(response.data, serializer.data)
