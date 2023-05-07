from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from booking.models import Discount
from django.test import override_settings



@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.AllowAllUsersModelBackend'])
class CheckPromocodeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create an event
        self.event_id = 1

        # create a discount for the event
        self.discount = Discount.objects.create(
            EVENT_ID=self.event_id,
            percent_off=25,
            CODE='SAVE123',
            start_date='2023-05-01',
            end_date='2023-05-31',
            Quantity_available=10,
            User_ID=1
        )

    def test_check_promocode_valid(self):
        """
        Test that a valid promocode is correctly identified.
        """
        url = reverse('check-promocode', args=[self.event_id])
        response = self.client.get(url, {'promocode': 'SAVE123'},follow=True)

        # assert that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the response data indicates the promocode is valid
        self.assertEqual(response.data, {'is_promocode': True})

    def test_check_promocode_invalid(self):
        """
        Test that an invalid promocode is correctly identified.
        """
        url = reverse('check-promocode', args=[self.event_id])
        response = self.client.get(url, {'promocode': 'INVALID'},follow=True)

        # assert that the response status code is HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert that the response data indicates the promocode is invalid
        self.assertEqual(response.data, {'is_promocode': False})

    def test_check_promocode_missing_param(self):
        """
        Test that missing promocode parameter is correctly identified.
        """
        url = reverse('check-promocode', args=[self.event_id])
        response = self.client.get(url,follow=True)

        # assert that the response status code is HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert that the response data indicates the missing promocode parameter error
        self.assertEqual(response.data, {'err': 'missing promocode param'})




