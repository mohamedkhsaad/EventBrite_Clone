from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from event.models import event
from booking.models import TicketClass


class FreeTicketEventListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event1 = event.objects.create(
            ID=1,
            Title='Event 1',
            organizer='Organizer 1',
            Summery='Summary 1',
            Description='Description 1',
            type='Type 1',
            category_name='Category 1',
            sub_Category='Sub-category 1',
            venue_name='Venue 1',
            ST_DATE='2022-05-01',
            END_DATE='2022-05-02',
            ST_TIME='09:00',
            END_TIME='17:00',
            online='Yes',
            CAPACITY=100,
            STATUS='Live'
        )
        self.event2 = event.objects.create(
            ID=2,
            Title='Event 2',
            organizer='Organizer 2',
            Summery='Summary 2',
            Description='Description 2',
            type='Type 2',
            category_name='Category 2',
            sub_Category='Sub-category 2',
            venue_name='Venue 2',
            ST_DATE='2022-06-01',
            END_DATE='2022-06-02',
            ST_TIME='09:00',
            END_TIME='17:00',
            online='Yes',
            CAPACITY=50,
            STATUS='Live'
        )
        self.ticket_class1 = TicketClass.objects.create(
            ID=1,
            event_id=self.event1.ID,
            NAME='Ticket Class 1',
            PRICE=10.0,
            capacity=50,
            quantity_sold=20,
            TICKET_TYPE='Paid',
            Sales_start='2022-04-01',
            Sales_end='2022-05-01',
            Start_time='10:00',
            End_time='12:00',
            Absorb_fees='True'
        )
        self.ticket_class2 = TicketClass.objects.create(
            ID=2,
            event_id=self.event1.ID,
            NAME='Ticket Class 2',
            PRICE=0.0,
            capacity=50,
            quantity_sold=10,
            TICKET_TYPE='Free',
            Sales_start='2022-04-01',
            Sales_end='2022-05-01',
            Start_time='10:00',
            End_time='12:00'
        )
        self.ticket_class3 = TicketClass.objects.create(
            ID=3,
            event_id=self.event2.ID,
            NAME='Ticket Class 3',
            PRICE=5.0,
            capacity=50,
            quantity_sold=0,
            TICKET_TYPE='Free',
            Sales_start='2022-05-01',
            Sales_end='2022-06-01',
            Start_time='10:00',
            End_time='12:00',
            Absorb_fees='False'
        )

    def test_get_free_ticket_events(self):
        url = reverse('free_event_list')
        response = self.client.get(url, format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)

