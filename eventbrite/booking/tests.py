from django.urls import reverse
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Ticket,Discount
from .serializers import TicketSerializer,DiscountSerializer
import json




class DiscountListTestCase(APITestCase):
    def setUp(self):
        self.discount1 = Discount.objects.create(
            ID=1, EVENT_ID=11111,
            percent_off='20%', CODE='DISCOUNT20',
            start_date='2022-01-01', end_date='2022-12-31',
            Quantity_available=100, User_ID=1)
        self.discount2 = Discount.objects.create(
            ID=2, EVENT_ID=11111,
            percent_off='30%', CODE='DISCOUNT30',
            start_date='2022-01-01', end_date='2022-12-31',
            Quantity_available=200, User_ID=2)
        self.url = reverse('discount-list')

    def test_list_discounts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['ID'], self.discount1.ID)
        self.assertEqual(response.data[1]['ID'], self.discount2.ID)

    def test_create_discount(self):
        data = {
            'ID': 3, 'EVENT_ID': 11111,
            'percent_off': '10%', 'CODE': 'DISCOUNT10',
            'start_date': '2022-01-01', 'end_date': '2022-12-31',
            'Quantity_available': 50, 'User_ID': 3
        }

        response = self.client.post(self.url, data)
        serialized_data = DiscountSerializer(Discount.objects.get(ID=3)).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serialized_data)

# class GetTicketTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.ticket1 = Ticket.objects.create(
#             ID=123, NAME='Test Ticket 1',
#            PRICE=20.0, EVENT_ID=10, GUEST_ID=15,
#             TICKET_NUM=5)
#         self.ticket2 = Ticket.objects.create(
#             ID=456, NAME='Test Ticket 2',
#            PRICE=100.0, EVENT_ID=20, GUEST_ID=25,
#             TICKET_NUM=1)

#     def test_get_ticket(self):
#         url = reverse('get-ticket', kwargs={'ticket_id': self.ticket1.ID})
#         response = self.client.get(url)
#         ticket = Ticket.objects.get(id=self.ticket1.ID)
#         serializer = TicketSerializer(ticket)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
 

    # def test_invalid_ticket(self):
    #     url = reverse('get-ticket', args=[999])
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
# where the ticket model is as follows:
# class Ticket(models.Model):
#     ID=models.IntegerField()
#     NAME=models.CharField(max_length=20)
#     PRICE=models.FloatField()
#     EVENT_ID=models.IntegerField()
#     GUEST_ID=models.IntegerField()
#     TICKET_NUM=models.IntegerField()
#     TICKET_TYPE=models.Choices("Free","VIP")


