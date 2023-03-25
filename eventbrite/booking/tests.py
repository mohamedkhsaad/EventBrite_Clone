from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from rest_framework.authtoken.models import Token

from .models import Ticket,Discount
from .serializers import TicketSerializer,DiscountSerializer
import json



class GetTicketTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # auth credentials
        # self.user = User.objects.create_user(
        #             email='test@example.com',
        #             first_name='ahmed',
        #             last_name='omar',
        #             age=30,
        #             gender='Male',
        #             city='cairo',
        #             country='egypyt'
        #             password='password',
        # )
        # self.token = Token.objects.create(user=self.user)

        # self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.ticket = Ticket.objects.create(
            ID=1,
            NAME='General Admission',
            PRICE=10.99,
            EVENT_ID=11111,
            GUEST_ID=1,
            TICKET_NUM=100
        )
        self.url = reverse('get-ticket', kwargs={'ticket_id': self.ticket.pk})

    def test_get_valid_ticket(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = TicketSerializer(self.ticket).data
        self.assertEqual(response.data, serialized_data)

    def test_get_invalid_ticket(self):
        url = reverse('get-ticket', kwargs={'ticket_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




class ListTicketsByEventTestCase(TestCase):
    def setUp(self):
        
        # auth credentials
        # self.user = User.objects.create_user(
        #             email='test@example.com',
        #             first_name='ahmed',
        #             last_name='omar',
        #             age=30,
        #             gender='Male',
        #             city='cairo',
        #             country='egypyt',
        #             password='password',
        # )
        # self.client = APIClient()

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        self.event_id = 12345
        self.ticket1 = Ticket.objects.create(
            ID=1,
            NAME='General Admission',
            PRICE=10.99,
            EVENT_ID=self.event_id,
            GUEST_ID=1,
            TICKET_NUM=100
        )
        self.ticket2 = Ticket.objects.create(
            ID=2,
            NAME='VIP',
            PRICE=25.99,
            EVENT_ID=self.event_id,
            GUEST_ID=2,
            TICKET_NUM=50
        )
        self.url = reverse('list-tickets-by-event', kwargs={'event_id': self.event_id})

    def test_list_tickets_by_event(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = TicketSerializer([self.ticket1, self.ticket2], many=True).data
        self.assertEqual(response.data, serialized_data)




class ListTicketsByUserTestCase(TestCase):
    def setUp(self):
        # self.client = APIClient()


        # auth credentials
        # self.user = User.objects.create_user(
        #             email='test@example.com',
        #             first_name='ahmed',
        #             last_name='omar',
        #             age=30,
        #             gender='Male',
        #             city='cairo',
        #             country='egypyt'
        #             password='password',
        # )
        # self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.user_id = 123
        self.ticket1 = Ticket.objects.create(
            ID=1,
            NAME='General Admission',
            PRICE=10.99,
            EVENT_ID=11111,
            GUEST_ID=self.user_id,
            TICKET_NUM=100
        )
        self.ticket2 = Ticket.objects.create(
            ID=2,
            NAME='VIP',
            PRICE=25.99,
            EVENT_ID=22222,
            GUEST_ID=self.user_id,
            TICKET_NUM=50
        )
        self.url = reverse('list-tickets-by-user', kwargs={'user_id': self.user_id})

    def test_list_tickets_by_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = TicketSerializer([self.ticket1, self.ticket2], many=True).data
        self.assertEqual(response.data, serialized_data)




class CheckPromoCodeTests(APITestCase):

    def setUp(self):


        # auth credentials
        # self.user = User.objects.create_user(
        #             email='test@example.com',
        #             first_name='ahmed',
        #             last_name='omar',
        #             age=30,
        #             gender='Male',
        #             city='cairo',
        #             country='egypyt'
        #             password='password',
        # )
        # self.token = Token.objects.create(user=self.user)
         
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        # Create a Discount object to use in the test
        self.discount = Discount.objects.create(
            ID=1,
            EVENT_ID=1,
            percent_off='50',
            CODE='SAVE50',
            start_date='2022-01-01',
            end_date='2022-01-31',
            Quantity_available=100,
            User_ID=1,
        )

    def test_check_promo_code_with_valid_code(self):
        """
        Test that a valid promo code for the specified event returns a 200 OK response.
        """
        url = reverse('check-promocode', kwargs={'event_id': 1})
        data = {'promo_code': 'SAVE50'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_promo_code'], True)


    def test_check_promo_code_with_missing_param(self):
        """
        Test that a missing promo code param returns a 400 Bad Request response.
        """
        url = reverse('check-promocode', kwargs={'event_id': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['err'], 'missing promo_code param')


class DiscountListTestCase(APITestCase):
    def setUp(self):


        # auth credentials
        # self.user = User.objects.create_user(
        #             email='test@example.com',
        #             first_name='ahmed',
        #             last_name='omar',
        #             age=30,
        #             gender='Male',
        #             city='cairo',
        #             country='egypyt'
        #             password='password',
        # )
        # self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        

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


# class DiscountPKTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.discount = Discount.objects.create(
#             ID=1,
#             EVENT_ID=11111,
#             percent_off='20%',
#             CODE='DISCOUNT123',
#             start_date='2023-03-22',
#             end_date='2023-03-28',
#             Quantity_available=100,
#             User_ID=1
#         )
#         self.url = f'/booking/discount/{self.discount.pk}/'

#     def test_retrieve_discount(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['ID'], self.discount.ID)
#         self.assertEqual(response.data['EVENT_ID'], self.discount.EVENT_ID)
#         self.assertEqual(response.data['percent_off'], self.discount.percent_off)
#         self.assertEqual(response.data['CODE'], self.discount.CODE)
#         self.assertEqual(response.data['start_date'], str(self.discount.start_date))
#         self.assertEqual(response.data['end_date'], str(self.discount.end_date))
#         self.assertEqual(response.data['Quantity_available'], self.discount.Quantity_available)
#         self.assertEqual(response.data['User_ID'], self.discount.User_ID)

#     def test_update_discount(self):
#         data = {
#             'percent_off': '30%',
#             'CODE': 'NEWCODE123',
#             'Quantity_available': 50
#         }
#         response = self.client.patch(self.url, data=data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.discount.refresh_from_db()
#         self.assertEqual(self.discount.percent_off, '30%')
#         self.assertEqual(self.discount.CODE, 'NEWCODE123')
#         self.assertEqual(self.discount.Quantity_available, 50)

#     def test_delete_discount(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Discount.objects.filter(pk=self.discount.pk).exists())



