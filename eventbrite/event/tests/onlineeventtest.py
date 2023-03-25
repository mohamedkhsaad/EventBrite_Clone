from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from event.views import OnlineEventsAPIView
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate


class OnlineEventsAPIViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        event1 = event.objects.create(
            ID="1001", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="music", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")

        event2 = event.objects.create(
            ID="10111", User_id="3", Title="Test Event", organizer="test",
            Description="test", type="music", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE="2023-03-23", END_DATE="2023-04-23", ST_TIME="05:00:00",
            END_TIME="09:00:00", online="f", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")
        self.url = reverse('online-events')

    def test_get_online_events(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = OnlineEventsAPIView.as_view()(request)
        events = event.objects.filter(online='t')
        serializer = eventSerializer(events, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
