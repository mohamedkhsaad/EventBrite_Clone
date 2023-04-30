# from django.urls import reverse
# from django.test import TestCase, Client, RequestFactory
# from django.contrib.auth import get_user_model
# from django.core import mail

# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from user.models import User
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

# from .models import Ticket,Discount
# from .serializers import TicketSerializer,DiscountSerializer
# import json

# from unittest.mock import patch

# import logging

# # Configure the logging module
# # logging.basicConfig(
# #     level=logging.DEBUG, # Set the logging level
# #     format='%(asctime)s %(levelname)s %(message)s', # Set the logging format
# #     handlers=[
# #         logging.FileHandler('debug.log'), # Log to a file
# #         logging.StreamHandler() # Log to the console
# #     ]
# # )


# #TODO: problem in len(mail.outbox)
# class CreateTicketAndSendConfirmationEmailTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass', email='testmail@example.com')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        
        
#         self.client.login(username='testuser', password='testpassword')

#         self.ticket_data = {
#             'ID': 1,
#             'NAME': 'Test Ticket',
#             'PRICE': 10.99,
#             'EVENT_ID': 1,
#             'GUEST_ID': 1,
#             'TICKET_NUM': 100,
#             'TICKET_TYPE': 'FREE'
#         }
#         self.ticket_url = reverse('create-ticket')

#     @patch('requests.get')
#     def test_create_ticket_and_send_confirmation_email(self, mock_get):
#         # Mock the Google Charts API response
#         mock_get.return_value.content = b'test_qr_code_image'

#         # Send a POST request to create a new ticket
#         response = self.client.post(self.ticket_url, self.ticket_data)

#         # Check that the response status code is 201 CREATED
#         self.assertEqual(response.status_code, 201)

#         # Check that a new ticket was created with the correct data
#         ticket = Ticket.objects.get(ID=self.ticket_data['ID'])
#         self.assertEqual(ticket.NAME, self.ticket_data['NAME'])
#         self.assertEqual(ticket.PRICE, self.ticket_data['PRICE'])
#         self.assertEqual(ticket.EVENT_ID, self.ticket_data['EVENT_ID'])
#         self.assertEqual(ticket.GUEST_ID, self.ticket_data['GUEST_ID'])
#         self.assertEqual(ticket.TICKET_NUM, self.ticket_data['TICKET_NUM'])
#         # self.assertEqual(ticket.TICKET_TYPE, self.ticket_data['TICKET_TYPE']) 

#         # Call the send_confirmation_email function
#         email_url = reverse('confirm-mail')
#         response = self.client.get(email_url)

#         # Check that the function returned a successful HTTP response
#         self.assertEqual(response.status_code, 201)

#         # Check that the email was sent to the correct recipient
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].to, [self.user.email])

#         # Check that the email contains the correct subject and message
#         self.assertEqual(mail.outbox[0].subject, 'Confirm your email address')
#         self.assertIn('Hi testuser, please click the link below or scan the QR code to confirm your ticket:', mail.outbox[0].body)
#         # self.assertIn(confirmation_url, mail.outbox[0].body)

#         # Check that the email contains the QR code image as an attachment
#         self.assertEqual(len(mail.outbox[0].attachments), 1)
#         self.assertEqual(mail.outbox[0].attachments[0][0], 'qrcode.png')
#         self.assertEqual(mail.outbox[0].attachments[0][2], 'image/png')
#         self.assertEqual(mail.outbox[0].attachments[0][1], b'test_qr_code_image')

#         # Check that the email contains the QR code image as an inline image
#         # self.assertIn('cid:qrcode', mail.outbox[0].alternatives[0][0])



# class SendConfirmationEmailTest(TestCase):
#     @patch('requests.get')
#     def test_send_confirmation_email(self, mock_get):
#         # Create a user and log them in
#         self.client = APIClient()

#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass', email='testmail@example.com')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        
        
        
#         self.client.login(username='testuser', password='testpassword')

#         # Mock the Google Charts API response
#         mock_get.return_value.content = b'test_qr_code_image'

#         # Call the send_confirmation_email function
#         response = self.client.get(reverse('confirm-mail'))

#         # Check that the function returned a successful HTTP response
#         self.assertEqual(response.status_code, 201)

#         # Check that the email was sent to the correct recipient
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].to, [self.user.email])

#         # Check that the email contains the correct subject and message
#         self.assertEqual(mail.outbox[0].subject, 'Confirm your email address')
#         self.assertIn('Hi testuser, please click the link below or scan the QR code to confirm your ticket:', mail.outbox[0].body)
#         # self.assertIn(confirmation_url, mail.outbox[0].body)

#         # Check that the email contains the QR code image as an attachment
#         self.assertEqual(len(mail.outbox[0].attachments), 1)
#         self.assertEqual(mail.outbox[0].attachments[0][0], 'qrcode.png')
#         self.assertEqual(mail.outbox[0].attachments[0][2], 'image/png')
#         self.assertEqual(mail.outbox[0].attachments[0][1], b'test_qr_code_image')

#         # Check that the email contains the QR code image as an inline image
#         # self.assertIn('cid:qrcode', mail.outbox[0].alternatives[0][0])


# #TODO: problem in checking ticket type

# class CreateTicketTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass', email='testmail@example.com')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        
        
        
#         self.client.login(username='testuser', password='testpassword')

#         self.data = {
#             'ID': 1,
#             'NAME': 'Test Ticket',
#             'PRICE': 10.99,
#             'EVENT_ID': 1,
#             'GUEST_ID': 1,
#             'TICKET_NUM': 100,
#             'TICKET_TYPE': 'FREE'
#         }
#         self.url = reverse('create-ticket')

#     def test_create_ticket(self):

#         # Send a POST request to create a new ticket
#         response = self.client.post(self.url, self.data)

#         # Check that the response status code is 201 CREATED
#         self.assertEqual(response.status_code, 201)

#         # Check that a new ticket was created with the correct data
#         ticket = Ticket.objects.get(ID=self.data['ID'])
#         self.assertEqual(ticket.NAME, self.data['NAME'])
#         self.assertEqual(ticket.PRICE, self.data['PRICE'])
#         self.assertEqual(ticket.EVENT_ID, self.data['EVENT_ID'])
#         self.assertEqual(ticket.GUEST_ID, self.data['GUEST_ID'])
#         self.assertEqual(ticket.TICKET_NUM, self.data['TICKET_NUM'])
#         self.assertEqual(ticket.TICKET_TYPE, self.data['TICKET_TYPE']) 





# # class GetTicketTestCase(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()

# #         # auth credentials
# #         # self.user = User.objects.create_user(
# #         #             email='test@example.com',
# #         #             first_name='ahmed',
# #         #             last_name='omar',
# #         #             age=30,
# #         #             gender='Male',
# #         #             city='cairo',
# #         #             country='egypyt'
# #         #             password='password',
# #         # )
# #         # self.token = Token.objects.create(user=self.user)

# #         # self.client = APIClient()
# #         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
# #         self.token = Token.objects.create(user=self.user)
# #         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

# #         self.ticket = Ticket.objects.create(
# #             ID=1,
# #             NAME='General Admission',
# #             PRICE=10.99,
# #             EVENT_ID=11111,
# #             GUEST_ID=1,
# #             TICKET_NUM=100
# #         )
# #         self.url = reverse('get-ticket', kwargs={'ticket_id': self.ticket.pk})

# #     def test_get_valid_ticket(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         serialized_data = TicketSerializer(self.ticket).data
# #         self.assertEqual(response.data, serialized_data)

# #     def test_get_invalid_ticket(self):
# #         url = reverse('get-ticket', kwargs={'ticket_id': 999})
# #         response = self.client.get(url)
# #         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




# # class ListTicketsByEventTestCase(TestCase):
# #     def setUp(self):
        
# #         # auth credentials
# #         # self.user = User.objects.create_user(
# #         #             email='test@example.com',
# #         #             first_name='ahmed',
# #         #             last_name='omar',
# #         #             age=30,
# #         #             gender='Male',
# #         #             city='cairo',
# #         #             country='egypyt',
# #         #             password='password',
# #         # )
# #         # self.client = APIClient()

# #         self.client = APIClient()
# #         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
# #         self.token = Token.objects.create(user=self.user)
# #         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


# #         self.event_id = 12345
# #         self.ticket1 = Ticket.objects.create(
# #             ID=1,
# #             NAME='General Admission',
# #             PRICE=10.99,
# #             EVENT_ID=self.event_id,
# #             GUEST_ID=1,
# #             TICKET_NUM=100
# #         )
# #         self.ticket2 = Ticket.objects.create(
# #             ID=2,
# #             NAME='VIP',
# #             PRICE=25.99,
# #             EVENT_ID=self.event_id,
# #             GUEST_ID=2,
# #             TICKET_NUM=50
# #         )
# #         self.url = reverse('list-tickets-by-event', kwargs={'event_id': self.event_id})

# #     def test_list_tickets_by_event(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         serialized_data = TicketSerializer([self.ticket1, self.ticket2], many=True).data
# #         self.assertEqual(response.data, serialized_data)




# # class ListTicketsByUserTestCase(TestCase):
# #     def setUp(self):
# #         # self.client = APIClient()


# #         # auth credentials
# #         # self.user = User.objects.create_user(
# #         #             email='test@example.com',
# #         #             first_name='ahmed',
# #         #             last_name='omar',
# #         #             age=30,
# #         #             gender='Male',
# #         #             city='cairo',
# #         #             country='egypyt'
# #         #             password='password',
# #         # )
# #         # self.token = Token.objects.create(user=self.user)

# #         self.client = APIClient()
# #         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
# #         self.token = Token.objects.create(user=self.user)
# #         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

# #         self.user_id = 123
# #         self.ticket1 = Ticket.objects.create(
# #             ID=1,
# #             NAME='General Admission',
# #             PRICE=10.99,
# #             EVENT_ID=11111,
# #             GUEST_ID=self.user_id,
# #             TICKET_NUM=100
# #         )
# #         self.ticket2 = Ticket.objects.create(
# #             ID=2,
# #             NAME='VIP',
# #             PRICE=25.99,
# #             EVENT_ID=22222,
# #             GUEST_ID=self.user_id,
# #             TICKET_NUM=50
# #         )
# #         self.url = reverse('list-tickets-by-user', kwargs={'user_id': self.user_id})

# #     def test_list_tickets_by_user(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         serialized_data = TicketSerializer([self.ticket1, self.ticket2], many=True).data
# #         self.assertEqual(response.data, serialized_data)




# class CheckPromoCodeTests(APITestCase):

#     def setUp(self):


#         # auth credentials
#         # self.user = User.objects.create_user(
#         #             email='test@example.com',
#         #             first_name='ahmed',
#         #             last_name='omar',
#         #             age=30,
#         #             gender='Male',
#         #             city='cairo',
#         #             country='egypyt'
#         #             password='password',
#         # )
#         # self.token = Token.objects.create(user=self.user)
         
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


#         # Create a Discount object to use in the test
#         self.discount = Discount.objects.create(
#             ID=1,
#             EVENT_ID=1,
#             percent_off='50',
#             CODE='SAVE50',
#             start_date='2022-01-01',
#             end_date='2022-01-31',
#             Quantity_available=100,
#             User_ID=1,
#         )

#     def test_check_promo_code_with_valid_code(self):
#         """
#         Test that a valid promo code for the specified event returns a 200 OK response.
#         """
#         url = reverse('check-promocode', kwargs={'event_id': 1})
#         data = {'promo_code': 'SAVE50'}
#         response = self.client.get(url, data, format='json',follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['is_promo_code'], True)


#     def test_check_promo_code_with_missing_param(self):
#         """
#         Test that a missing promo code param returns a 400 Bad Request response.
#         """
#         url = reverse('check-promocode', kwargs={'event_id': 1})
#         response = self.client.get(url, format='json',follow=True)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['err'], 'missing promo_code param')


# class DiscountListTestCase(APITestCase):
#     def setUp(self):


#         # auth credentials
#         # self.user = User.objects.create_user(
#         #             email='test@example.com',
#         #             first_name='ahmed',
#         #             last_name='omar',
#         #             age=30,
#         #             gender='Male',
#         #             city='cairo',
#         #             country='egypyt'
#         #             password='password',
#         # )
#         # self.token = Token.objects.create(user=self.user)

#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        

#         self.discount1 = Discount.objects.create(
#             ID=1, EVENT_ID=11111,
#             percent_off='20%', CODE='DISCOUNT20',
#             start_date='2022-01-01', end_date='2022-12-31',
#             Quantity_available=100, User_ID=1)
#         self.discount2 = Discount.objects.create(
#             ID=2, EVENT_ID=11111,
#             percent_off='30%', CODE='DISCOUNT30',
#             start_date='2022-01-01', end_date='2022-12-31',
#             Quantity_available=200, User_ID=2)
#         self.url = reverse('discount-list')

#     def test_list_discounts(self):
#         response = self.client.get(self.url,follow=True)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#         self.assertEqual(int(response.data[0]['ID']), self.discount1.ID)
#         self.assertEqual(int(response.data[1]['ID']), self.discount2.ID)

#     def test_create_discount(self):
#         data = {
#             'ID': 3, 'EVENT_ID': 11111,
#             'percent_off': '10%', 'CODE': 'DISCOUNT10',
#             'start_date': '2022-01-01', 'end_date': '2022-12-31',
#             'Quantity_available': 50, 'User_ID': 3
#         }

#         response = self.client.post(self.url, data,follow=True)
#         serialized_data = DiscountSerializer(Discount.objects.get(ID=3)).data

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, serialized_data)


# # class DiscountPKTestCase(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.discount = Discount.objects.create(
# #             ID=1,
# #             EVENT_ID=11111,
# #             percent_off='20%',
# #             CODE='DISCOUNT123',
# #             start_date='2023-03-22',
# #             end_date='2023-03-28',
# #             Quantity_available=100,
# #             User_ID=1
# #         )
# #         self.url = f'/booking/discount/{self.discount.pk}/'

# #     def test_retrieve_discount(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(response.data['ID'], self.discount.ID)
# #         self.assertEqual(response.data['EVENT_ID'], self.discount.EVENT_ID)
# #         self.assertEqual(response.data['percent_off'], self.discount.percent_off)
# #         self.assertEqual(response.data['CODE'], self.discount.CODE)
# #         self.assertEqual(response.data['start_date'], str(self.discount.start_date))
# #         self.assertEqual(response.data['end_date'], str(self.discount.end_date))
# #         self.assertEqual(response.data['Quantity_available'], self.discount.Quantity_available)
# #         self.assertEqual(response.data['User_ID'], self.discount.User_ID)

# #     def test_update_discount(self):
# #         data = {
# #             'percent_off': '30%',
# #             'CODE': 'NEWCODE123',
# #             'Quantity_available': 50
# #         }
# #         response = self.client.patch(self.url, data=data)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.discount.refresh_from_db()
# #         self.assertEqual(self.discount.percent_off, '30%')
# #         self.assertEqual(self.discount.CODE, 'NEWCODE123')
# #         self.assertEqual(self.discount.Quantity_available, 50)

# #     def test_delete_discount(self):
# #         response = self.client.delete(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# #         self.assertFalse(Discount.objects.filter(pk=self.discount.pk).exists())



