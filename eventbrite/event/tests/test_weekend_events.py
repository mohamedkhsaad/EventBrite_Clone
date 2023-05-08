from rest_framework import status
from event.views import *
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.test import RequestFactory
from django.urls import reverse
from datetime import date, timedelta


class Weekend_EventsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.today = date.today()
        today = timezone.now().date()
        friday = today + timezone.timedelta((4 - today.weekday()) % 7)
        saturday = friday + timezone.timedelta(1)
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
            ST_DATE=friday,
            END_DATE=saturday,
            ST_TIME='09:00:00',
            END_TIME='10:00:00',
            online='True',
            CAPACITY=50,
            STATUS='Live',
            image=None
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
            ST_DATE=friday,
            END_DATE=saturday,
            ST_TIME='10:00:00',
            END_TIME='11:00:00',
            online='False',
            CAPACITY=100,
            STATUS='Draft',
            image=None
        )
        self.event3 = event.objects.create(
            ID=3,
            User_id=3,
            Title='Online Event 2',
            organizer='Organizer 2',
            Summery='Summary 2',
            Description='Description 2',
            type='Type 2',
            category_name='Category 2',
            sub_Category='Sub-category 2',
            venue_name='Venue 2',
            ST_DATE=friday - timedelta(1),
            END_DATE=saturday + timedelta(1),
            ST_TIME='10:00:00',
            END_TIME='11:00:00',
            online='False',
            CAPACITY=100,
            STATUS='Draft',
            image=None
        )
        self.url2 = reverse('weekend-events')

    def test_weekend_get_queryset(self):
        request = self.factory.get(self.url2)
        response = WeekendEventsView.as_view()(request)
        serializer = eventSerializer([self.event1, self.event2], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        # Check that the response data contains the expected events
        expected_events = event.objects.filter(
            ST_DATE__gte=self.event1.ST_DATE,
            END_DATE__lte=self.event2.END_DATE
        )
        serialized_expected_events = eventSerializer(
            expected_events, many=True).data
        self.assertEqual(response.data, serialized_expected_events)
