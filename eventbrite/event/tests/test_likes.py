from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from event.models import *
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class LikeEventViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.event = event.objects.create(
            ID=1,
            User_id=1,
            Title='Test Event',
            organizer='Test Organizer',
            user=self.user,
            Summery='Test Summary',
            Description='Test Description',
            type='Type',
            category_name='Category',
            sub_Category='Subcategory',
            venue_name='Test Venue',
            ST_DATE=datetime.today(),
            END_DATE=datetime.today() + timedelta(days=1),
            ST_TIME=datetime.now().strftime('%H:%M:%S'),
            END_TIME=(datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S'),
            online='Online',
            CAPACITY=100,
            STATUS='Open',
        )

    def test_follow_event_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('like-event', args=[self.event.ID])
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['status'],'success')

    def test_follow_event_unauthenticated(self):
        url = reverse('like-event', args=[self.event.ID])
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['status'], 'error')
        # self.assertEqual(response.data, {'status': 'error', 'message': 'You must be logged in to follow an event.'})



class UserLikedEventsTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.event = event.objects.create(
            ID=1,
            User_id=1,
            Title='Test Event',
            organizer='Test Organizer',
            user=self.user,
            Summery='Test Summary',
            Description='Test Description',
            type='Type',
            category_name='Category',
            sub_Category='Subcategory',
            venue_name='Test Venue',
            ST_DATE=datetime.today(),
            END_DATE=datetime.today() + timedelta(days=1),
            ST_TIME=datetime.now().strftime('%H:%M:%S'),
            END_TIME=(datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S'),
            online='Online',
            CAPACITY=100,
            STATUS='Open',
        )
        self.event_follower = Eventlikes.objects.create(
            user=self.user, event=self.event, ID=self.event.ID
        )

    def test_user_likes_events_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-liked-events')
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['Title'], self.event.Title)

    def test_user_likes_events_unauthenticated(self):
        url = reverse('user-liked-events')
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(
            response.data['message'], 'You must be logged in to see followed events.'
        )


