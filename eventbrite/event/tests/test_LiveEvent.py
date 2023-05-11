from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from event.views import *
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
class LiveEventsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event1 = event.objects.create(
            ID=1,
            User_id=1,
            Title='Online Event 1',
            organizer='Organizer 1',
            Summery='Summary 1',
            Description='Description 1',
            type='Type 1',
            category_name='Category 1',
            sub_Category='Sub-category 1',
            venue_name='Venue 1',
            ST_DATE='2023-04-15',
            END_DATE='2023-04-15',
            ST_TIME='09:00:00',
            END_TIME='10:00:00',
            online='True',
            CAPACITY=50,
            STATUS='Live',
            image='eventbrite/media/events/photo-1533450718592-29d45635f0a9_H6X4vcW.jpeg'
        )
        self.event2 = event.objects.create(
            ID=2,
            User_id=2,
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
            image='eventbrite/media/events/photo-1533450718592-29d45635f0a9_H6X4vcW.jpeg'
        )
        self.url = reverse('Live_event_list')
    def test_get_live_events(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = LiveEventsAPIView.as_view()(request)
        events = event.objects.filter(STATUS='Live')
        serializer = eventSerializer(events, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)