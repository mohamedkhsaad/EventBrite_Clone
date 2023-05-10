from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from event.models import event
from booking.models import TicketClass
from booking.serializers import TicketQuantityClassSerializer
from user.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model
from django.test import  RequestFactory
from rest_framework.test import force_authenticate

class QuantitySoldOutOfTotalTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='daniel',
            email='dani@gmail.com',
            password='Daniel&889',)
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
            image=None
        )
        self.event2 = event.objects.create(
            ID=987668,
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
            STATUS='Draft',
            image=None
        )
        self.event_ID=1

def test_quantity_sold_out_of_total(self):
        # Create test data
        url = reverse('sold_tickets', kwargs={'event_id': self.event_ID})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)

        ticket_classes = TicketClass.objects.filter(event_id=self.event_ID)
        serializer = TicketQuantityClassSerializer(ticket_classes, many=True)
        self.assertEqual(response.data, serializer.data)