from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import event
from datetime import date, time
from rest_framework import status
from .serializers import *


class EventManagementTest(APITestCase):
    
    
    def setUp(self):
        
        eventus = event.objects.create(ID= 1, User_id=1190507, Title="mmatalk", organizer='Abdelrhman Elshahed', Description="mmatalk", type="chatting", Category='sport', sub_Category='mma', venue_name='giza', CATEGORY_ID=1, SUB_CATEGORY_ID=1, ST_DATE=date(2023, 3, 5), END_DATE=date(2023, 4, 1), ST_TIME=time(15, 00, 00), END_TIME=time(16, 00, 00), ONLINE=True, CAPACITY=500, PASSWORD=123456, location_id=1, STATUS='open')





    def test_retrieve_all_user_events_by_user_id(self):
        self.client = APIClient()
        user_id = 1190507
        eventus = event.objects.filter(User_id= user_id)
        serializer = eventSerializer(eventus, many=True)
        url = f"http://127.0.0.1:8000/events/list_user_events/{user_id}/"
        response = self.client.get(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response, serializer.data)

    def test_retrieve_all_user_past_events_by_user_id(self):
        self.client = APIClient()
        user_id = 1190507
        today = date.today()
        eventus = event.objects.filter(User_id=user_id).filter(ST_DATE__lt=today)
        serializer = eventSerializer(eventus, many=True)
        url = {f'http://127.0.0.1:8000/events/list_user_past_events/{user_id}/'}
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response, serializer.data)

    def test_retrieve_all_user_upcoming_events_by_user_id(self):
        self.client = APIClient()
        user_id = 1190507
        today = date.today()
        eventus = event.objects.filter(User_id=user_id).filter(ST_DATE__gt=today)
        serializer = eventSerializer(eventus, many=True)
        url = {f'http://127.0.0.1:8000/events/list_user_past_events/{user_id}/'}
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response, serializer.data)
