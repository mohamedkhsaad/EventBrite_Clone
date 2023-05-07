from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from booking.models import Discount, Order, OrderItem, TicketClass
from event.models import event as Event
from booking.serializers import OrderItemSerializer

# class CreateOrderTestCase(APITestCase):
#     def setUp(self):
#         self.event_id = 1
#         self.ticket_class_1 = TicketClass.objects.create(event_id=self.event_id, NAME='Test Ticket 1', PRICE=20, capacity=10)
#         self.ticket_class_2 = TicketClass.objects.create(event_id=self.event_id, NAME='Test Ticket 2', PRICE=10, capacity=5)

#     def test_create_order(self):
#         url = reverse('create-order', kwargs={'event_id': self.event_id})
#         data = {
#             "order_items": [
#                 {"ticket_class_id": self.ticket_class_1.id, "quantity": 3},
#                 {"ticket_class_id": self.ticket_class_2.id, "quantity": 1}
#             ],
#             "promocode": "DISCOUNT25",
#             "user_id": 1
#         }
#         response = self.client.post(url, data, format='json',follow=True)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Check that an order and order items were created
#         self.assertEqual(Order.objects.count(), 1)
#         self.assertEqual(OrderItem.objects.count(), 2)

#         # Check the data in the order
#         order = Order.objects.get()
#         self.assertEqual(order.event_id, self.event_id)
#         self.assertEqual(order.user_id, 1)
#         self.assertEqual(order.full_price, 70.0)
#         self.assertEqual(order.amount_off, 17.5)
#         self.assertEqual(order.fee, 0)
#         self.assertEqual(order.total, 52.5)

#         # Check the data in the order items
#         order_item_1 = OrderItem.objects.get(ticket_class_id=self.ticket_class_1.id)
#         self.assertEqual(order_item_1.order_id, order.ID)
#         self.assertEqual(order_item_1.ticket_price, 20.0)
#         self.assertEqual(order_item_1.currency, 'USD')
#         self.assertEqual(order_item_1.quantity, 3)
#         self.assertEqual(order_item_1.user_id, 1)
#         self.assertEqual(order_item_1.event_id, self.event_id)

#         order_item_2 = OrderItem.objects.get(ticket_class_id=self.ticket_class_2.id)
#         self.assertEqual(order_item_2.order_id, order.ID)
#         self.assertEqual(order_item_2.ticket_price, 10.0)
#         self.assertEqual(order_item_2.currency, 'USD')
#         self.assertEqual(order_item_2.quantity, 1)
#         self.assertEqual(order_item_2.user_id, 1)
#         self.assertEqual(order_item_2.event_id, self.event_id)

#         # Check that the ticket classes were updated
#         self.ticket_class_1.refresh_from_db()
#         self.assertEqual(self.ticket_class_1.quantity_sold, 3)

#         self.ticket_class_2.refresh_from_db()
#         self.assertEqual(self.ticket_class_2.quantity_sold, 1)



# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status

# class CreateOrderTestCase(APITestCase):
#     def setUp(self):
#         self.event_id = 1
#         self.ticket_class1 = TicketClass.objects.create(
#             id=1,
#             event_id=self.event_id,
#             name='Class 1',
#             quantity_sold=0,
#             capacity=5,
#             price=10.0
#         )
#         self.ticket_class2 = TicketClass.objects.create(
#             id=2,
#             event_id=self.event_id,
#             name='Class 2',
#             quantity_sold=0,
#             capacity=5,
#             price=20.0
#         )

#     def test_create_order(self):
#         url = reverse('create-order', args=[self.event_id])
#         data = {
#             "order_items": [
#                 {
#                     "ticket_class_id": self.ticket_class1.id,
#                     "quantity": 2
#                 },
#                 {
#                     "ticket_class_id": self.ticket_class2.id,
#                     "quantity": 1
#                 }
#             ],
#             "promocode": "DISCOUNT25",
#             "user_id": 1
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['full_price'], 40.0)
#         self.assertEqual(response.data['amount_off'], 10.0)
#         self.assertEqual(response.data['fee'], 0.0)
#         self.assertEqual(response.data['total'], 30.0)
#         self.assertEqual(Order.objects.count(), 1)
#         self.assertEqual(OrderItem.objects.count(), 2)
#         self.assertEqual(TicketClass.objects.get(id=self.ticket_class1.id).quantity_sold, 2)
#         self.assertEqual(TicketClass.objects.get(id=self.ticket_class2.id).quantity_sold, 1)

#     def test_create_order_with_invalid_promocode(self):
#         url = reverse('create-order', args=[self.event_id])
#         data = {
#             "order_items": [
#                 {
#                     "ticket_class_id": self.ticket_class1.id,
#                     "quantity": 2
#                 }
#             ],
#             "promocode": "INVALID",
#             "user_id": 1
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['details'], 'there isnt any discount with this promocode and event id')
#         self.assertEqual(Order.objects.count(), 0)
#         self.assertEqual(OrderItem.objects.count(), 0)
#         self.assertEqual(TicketClass.objects.get(id=self.ticket_class1.id).quantity_sold, 0)

#     def test_create_order_with_insufficient_tickets(self):
#         url = reverse('create-order', args=[self.event_id])
#         data = {
#             "order_items": [
#                 {
#                     "ticket_class_id": self.ticket_class1.id,
#                     "quantity": 10
#                 }
#             ],
#             "promocode": "DISCOUNT25",
#             "user_id": 1
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['details'], f'Not enough tickets available for ticket class id {self.ticket_class1.id}')
#         self.assertEqual(Order.objects.count(), 0)
#         self.assertEqual(OrderItem.objects.count(), 0)
#         self.assertEqual(TicketClass.objects.get(id=self.ticket_class1.id).quantity_sold, 0)
