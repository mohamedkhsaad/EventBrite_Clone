from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from event.models import *


class EventListVenueTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event = event.objects.create(
            ID=1,
            User_id=1,
            Title='Test Event',
            organizer=self.user,
            user=self.user,
            Summery='Test Event Summery',
            Description='Test Event Description',
            type='Test Event Type',
            category_name='Test Event Category',
            sub_Category='Test Event Sub-Category',
            venue_name='Venue 1',
            ST_DATE='2023-05-15',
            END_DATE='2023-05-16',
            ST_TIME='10:00:00',
            END_TIME='18:00:00',
            online='True',
            CAPACITY=100,
            PASSWORD='test',
            STATUS='Live',
            image=None
        )
        self.event_venue = 'Venue 1'

    def test_event_list_by_venue(self):
        url = reverse('event-list-by-venue',
                      kwargs={'event_venue': self.event.venue_name})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_event_list_by_nonexistent_venue(self):
        nonexistent_venue = 'nonexistent venue'
        url = reverse('event-list-by-venue',
                      kwargs={'event_venue': nonexistent_venue})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
