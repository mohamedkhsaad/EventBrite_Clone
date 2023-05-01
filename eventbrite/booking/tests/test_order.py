from django.test import TestCase
from decimal import Decimal
from rest_framework.test import APIClient
from booking.models import *
from booking.serializers import *



from django.test import TestCase
from booking.models import *
from booking.serializers import OrderSerializer, OrderItemSerializer




class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ticket_class_1 = TicketClass.objects.create(name='Apple', price=Decimal('1.99'))
        self.order_data = {
            'customer_name': 'John Doe',
            'items': [
                {
                    'ticket_class_1': self.ticket_class_1.id,
                    'quantity': 2
                }
            ]
        }

    def test_create_order(self):
        url = reverse('create_order')
        response = self.client.post(url, data=self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get()
        self.assertEqual(order.customer_name, 'John Doe')
        self.assertEqual(order.total_price, Decimal('3.98'))
        order_item = order.items.first()
        self.assertEqual(order_item.fruit_type, self.ticket_class_1)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('1.99'))



# class OrderSerializerTestCase(TestCase):
#     def setUp(self):
#         x=0
#         self.user = User.objects.create(username='testuser')
#         # self.user.save()
#         self.event = event.objects.create(ID=1, Title='Test Event')
#         # self.event.save()
#         self.ticket_class_1 = TicketClass.objects.create(
#             event=self.event,
#             name='VIP Ticket',
#             price=100,
#             capacity=10,
#             quantity_sold=5,
#             ticket_type='Paid'
#         )   
#         # self.ticket_class_1.save()  

#         self.ticket_class_2 = TicketClass.objects.create(
#             event=self.event,
#             name='VIP Ticket high',
#             price=400,
#             capacity=50,
#             quantity_sold=10,
#             ticket_type='Paid'
#         ) 
#         # self.ticket_class_2.save()

#         self.order=Order.objects.create(
#             id=1,
#             user=self.user,
#             event=self.event,
#             discount=None,
#             full_price=0,
#             fee=0,
#             total=0,
#             is_validated=False)
#         # self.order.save()


        
#         self.order_item_1 = OrderItem.objects.create(
#                 order = self.order,
#                 ticket_class=self.ticket_class_1,
#                 quantity=2,
#                 ticket_price=self.ticket_class_1.price,
#                 currency='USD')

#         # self.order_item_2 = OrderItem.objects.create(
#         #         order = self.order,
#         #         ticket_class=self.ticket_class_2,
#         #         quantity=20,
#         #         ticket_price=self.ticket_class_2.price,
#         #         currency='USD'
#         #     ),
            
#     def test_order_serializer(self):
#         self.assertTrue(True)

#     #     self.assertTrue(serializer.is_valid())
#     #     order = serializer.save()
#     #     self.assertEqual(order.user, self.user)
#     #     self.assertEqual(order.event, self.event)
#     #     self.assertEqual(order.discount, self.discount)
#     #     self.assertEqual(order.tickets_classes.count(), 1)

#     #     order_item = order.tickets_classes.first()
#     #     self.assertEqual(order_item.ticket_class, self.ticket_class)
#     #     self.assertEqual(order_item.quantity, 2)
#     #     self.assertEqual(order_item.ticket_price, self.ticket_class.price)
#     #     self.assertEqual(order_item.currency, 'USD')

#     #     # check calculated fields
#     #     self.assertEqual(order.full_price, Decimal('40.00'))
#     #     self.assertEqual(order.fee, Decimal('4.00'))
#     #     self.assertEqual(order.total, Decimal('44.00'))




# class TestTicketSerializer(TestCase):
#     def setUp(self):
#         self.ticket = TicketClass.objects.create(
#             event=event.objects.create(ID=1, Title='Test Event'),
#             name='VIP Ticket',
#             price=100,
#             capacity=10,
#             quantity_sold=5,
#             ticket_type='Paid'
#         )
#         self.serializer = TicketSerializer(instance=self.ticket)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertEqual(set(data.keys()), set(['name', 'price', 'capacity', 'quantity_sold', 'ticket_type', 'Sales_start', 'Sales_end', 'Start_time', 'End_time', 'Absorb_fees']))

#     def test_name_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['name'], self.ticket.name)

#     def test_price_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['price'], self.ticket.price)



# class TestOrderItemSerializer(TestCase):
#     def setUp(self):
#         self.event = event.objects.create(ID=1, Title='Test Event')
#         self.ticket = TicketClass.objects.create(
#             event=self.event,
#             name='VIP Ticket',
#             price=100,
#             capacity=10,
#             quantity_sold=5,
#             ticket_type='Paid'
#         )


#         self.order_item = OrderItem.objects.create(
#             order=Order.objects.create(
#                 id=1,
#                 user=User.objects.create(username='testuser'),
#                 event=self.event,
#                 discount=None,
#                 full_price=0,
#                 fee=0,
#                 total=0,
#                 is_validated=False
#             ),
#             ticket_class=self.ticket,
#             quantity=2,
#             ticket_price=self.ticket.price,
#             currency='USD'
#         )
#         self.serializer = OrderItemSerializer

