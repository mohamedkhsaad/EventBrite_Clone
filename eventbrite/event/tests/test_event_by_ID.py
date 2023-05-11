
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from event.models import *
from eventManagment.models import *
from event.serializers import *
from booking.serializers import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

class EventIDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = event.objects.create(
            ID=1,
            User_id=1,
            Title='Online Event 2',
            organizer='Organizer 2',
            Summery='Summary 2',
            Description='Description 2',
            type='Type 2',
            category_name='Category 2',
            sub_Category='Sub-category 2',
            venue_name='Venue 2',
            ST_DATE='2023-04-16',
            END_DATE='2023-04-16',
            ST_TIME='10:00:00',
            END_TIME='11:00:00',
            online='False',
            CAPACITY=100,
            STATUS='Live',
            image=None
        )

    def test_retrieve_existing_event(self):
        url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
        response = self.client.get(url,follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, eventSerializer(self.event).data)

    def test_retrieve_nonexistent_event(self):
        url = reverse('event-list-by-ID', kwargs={'event_ID': 999})
        response = self.client.get(url,follow=True)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Event not found.'})

    # @patch('event.views.redirect')
    # def test_private_event_with_authenticated_user(self, mock_redirect):
    #     mock_user = self.client.post('/auth/token/login/', {
    #         'email': 'test@example.com',
    #         'password': 'Test_password12345*',
    #     })
    #     self.client.force_authenticate(user=mock_user)

    #     publish_info = Publish_Info.objects.create(
    #         Event_ID=self.event.ID,
    #         Event_Status='Private',
    #     )

    #     url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
    #     response = self.client.get(url,follow=True)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, eventSerializer(self.event).data)
    #     mock_redirect.assert_not_called()

    # @patch('your_app.views.redirect')
    # def test_private_event_with_unauthenticated_user(self, mock_redirect):
    #     publish_info = Publish_Info.objects.create(
    #         Event_ID=self.event.ID,
    #         Event_Status='Private',
    #         Audience_Password='test_password',
    #     )

    #     url = reverse('event_id', kwargs={'event_ID': self.event.ID})
    #     response = self.client.get(url)

    #     mock_redirect.assert_called_once_with(
    #         'check_password_view', event_id=self.event.ID)
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    # def test_private_event_authenticated_user(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertRedirects(response, reverse('check_password_view', args=[self.event.ID]))

    #     self.client.force_authenticate(user=self.event.user)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     serializer = eventSerializer(self.event)
    #     self.assertEqual(response.data, serializer.data)

    # def test_private_event_unauthenticated_user(self):
    #     response = self.client.P(self.url,follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertRedirects(response,reverse('check_password_view', args=[self.event.ID]))

    # def test_public_event(self):
    #     self.publish_info.Event_Status = 'Public'
    #     # self.publish_info.save()
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.get(self.url,follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     serializer = eventSerializer(self.event)
    #     self.assertEqual(response.data, serializer.data)
