from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from booking.models import Order

class OrderListViewTestCase(APITestCase):
    def setUp(self):
        self.user_id = 1
        self.order1 = Order.objects.create(user_id=self.user_id, full_price=10.0, total=10.0)
        self.order2 = Order.objects.create(user_id=self.user_id, full_price=20.0, total=20.0)

    def test_list_orders_by_user(self):
        url = reverse('list-orders-by-user', kwargs={'user_id': self.user_id})
        response = self.client.get(url,follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # self.assertEqual(response.data[0]['id'], self.order1.ID)
        self.assertEqual(response.data[0]['user_id'], self.user_id)
        self.assertEqual(response.data[0]['full_price'], 10.00)
        self.assertEqual(response.data[0]['total'], 10.00)
        self.assertEqual(response.data[0]['is_validated'], False)
        # self.assertEqual(response.data[1]['id'], self.order2.ID)
        self.assertEqual(response.data[1]['user_id'], self.user_id)
        self.assertEqual(response.data[1]['full_price'], 20.00)
        self.assertEqual(response.data[1]['total'], 20.00)
        self.assertEqual(response.data[1]['is_validated'], False)


