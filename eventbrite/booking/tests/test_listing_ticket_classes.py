from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from booking.models import *
from event.models import event as Event
from booking.serializers import *

import pytz
timezone = pytz.timezone('UTC')

from datetime import datetime


class ListTicketClassesByEventTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create a user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            age=25,
            gender='male',
            city='New York',
            country='USA',
            is_staff=True,
            is_active=True,
            username='testuser'
        )

        # create an event
        self.event = Event.objects.create(
            Title='Test Event',
            organizer=self.user,
            user=self.user,
            Summery='Test Summery',
            Description='Test Description',
            type='Test Type',
            category_name='Test Category',
            sub_Category='Test Sub Category',
            venue_name='Test Venue',
            ST_DATE='2023-05-03',
            END_DATE='2023-05-04',
            ST_TIME='10:00:00',
            END_TIME='12:00:00',
            online='True',
            CAPACITY=100,
            STATUS='Test Status'
        )

        # create a ticket class for the event
        self.ticket_class = TicketClass.objects.create(
            event_id=self.event.ID,
            User_id=self.user.id,
            NAME='Test Ticket Class',
            PRICE=50.00,
            capacity=10,
            quantity_sold=0,
            TICKET_TYPE='Paid',
            Sales_start=datetime(2023, 5, 3, 10, 0, 0, tzinfo=timezone),
            Sales_end=datetime(2023, 5, 8, 10, 0, 0, tzinfo=timezone),
            Start_time=datetime(2023, 5, 3, 10, 0, 0, tzinfo=timezone),
            End_time=datetime(2023, 5, 8, 10, 0, 0, tzinfo=timezone),
            Absorb_fees='True'
        )

        # set up authentication for the client
        self.client.force_authenticate(user=self.user)

    def test_list_ticket_classes_by_event(self):
        """
        Ensure we can list all ticket classes for an event.
        """
        url = f'/events/{self.event.ID}/ticket-classes/'
        response = self.client.get(url)

        # assert that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the response data matches the serialized ticket classes for the event
        expected_data = TicketClassSerializer([self.ticket_class], many=True).data
        self.assertEqual(response.data, expected_data)
