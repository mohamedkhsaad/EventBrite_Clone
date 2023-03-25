from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from event.models import event
from datetime import date, time
from rest_framework import status
from event.serializers import *
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from datetime import date, timedelta



class EventManagementTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user_id = 3
        self.today = date.today()
        self.past_date = self.today - timedelta(days=7)
        self.future_date = self.today + timedelta(days=7)

        self.event1 = event.objects.create(
            ID="10111",User_id=self.user_id , Title="Test Event", organizer="test",
            Description="test", type="music", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE=self.past_date,END_DATE=self.today, ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")
        
        self.event2 = event.objects.create(
            ID="102", User_id="5" , Title="Test Event", organizer="test",
            Description="test", type="food", Category="test", sub_Category="test", venue_name="test",
            CATEGORY_ID="5", SUB_CATEGORY_ID="7", ST_DATE=self.today, END_DATE= self.future_date , ST_TIME="05:00:00",
            END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="512002", locationـid="1", STATUS="test")


    def test_retrieve_all_user_events_by_user_id(self):
        url = reverse('user_list_events', kwargs={'user_id': self.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        event_data = response.data[0]
        serializer = eventSerializer(self.event1)
        self.assertEqual(event_data, serializer.data)


    # def test_retrieve_all_user_past_events_by_user_id(self):
    #     url = reverse('user_list_past_events', kwargs={'user_id': self.user_id})
    #     response = self.client.get(url)
    #     print()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     queryset = event.objects.filter(User_id=self.user_id,ST_DATE=self.today)
    #     serializer = eventSerializer(queryset, many=True)
    #     event_data = response.data[0]

    #     self.assertEqual(event_data, serializer.data)
    #     print(response.data)

#     def test_retrieve_all_user_upcoming_events_by_user_id(self):
#         self.client = APIClient()
#         user_id = 1190507
#         today = date.today()
#         eventus = event.objects.filter(
#             User_id=user_id).filter(ST_DATE__gt=today)
#         serializer = eventSerializer(eventus, many=True)
#         url = {f'http://127.0.0.1:8000/events/list_user_past_events/{user_id}/'}
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
#         self.assertEqual(response, serializer.data)