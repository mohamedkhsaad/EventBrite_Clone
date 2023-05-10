from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from event.models import event
from booking.models import Discount
from datetime import date
from rest_framework.authtoken.models import Token


class PromoCodeCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='banda@gmail.com',
            password='12345678',
            username='banda',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.event = event.objects.create(
            ID=1,
            User_id=self.user.id,
            Title="Test Event",
            organizer="test",
            Description="test",
            type="music",
            category_name="test",
            sub_Category="test",
            venue_name="test",
            ST_DATE=date.today(),
            END_DATE=date.today(),
            ST_TIME="05:00:00",
            END_TIME="09:00:00",
            online="t",
            CAPACITY="5000",
            STATUS="test"
        )
        self.discount = Discount.objects.create(
            ID=1,
            EVENT_ID=1,
            User_ID=self.user.id,
            CODE='TESTCODE',
            Ticket_limit='Limited',
            Limitedamount=100,
            Reveal_hidden='True',
            Discountـpercentage=20,
            Discount_price=0,
            Starts='now',
            Ends='scheduled',
            start_date=None,
            start_time=None,
            end_date=None,
            end_time=None,
            Quantity_available=100,
        )

    # def test_create_promocode_single(self):
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('create_promocode', kwargs={'event_id': self.event.ID})
    #     data = {
    #         'CODE': 'TESTCODE',
    #         'Ticket_limit': 'Limited',
    #         'Limitedamount': 100,
    #         'Discountـpercentage': 20,
    #     }
    #     response = self.client.post(url, data, format='json', follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Discount.objects.count(), 1)
    #     promo_code = Discount.objects.first()
    #     self.assertEqual(promo_code.EVENT_ID, self.event.ID)
    #     self.assertEqual(promo_code.User_ID, self.user.id)
    #     self.assertEqual(promo_code.CODE, 'TESTCODE')

    # def test_create_promocode_csv(self):
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('create_promocode', kwargs={'event_id': self.event.ID})
    #     csv_data = '''code,ticket_limit,limited_amount,discount_percentage
    #                   CODE1,Limited,10,100,20
    #                   CODE2,Limited,5,50,10'''
    #     file_obj = SimpleUploadedFile("promocodes.csv", csv_data.encode())
    #     data = {'file': file_obj}
    #     response = self.client.post(url, data, format='multipart', follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Discount.objects.count(), 2)
    #     promo_codes = Discount.objects.all()
    #     self.assertEqual(promo_codes[0].EVENT_ID, self.event.ID)
    #     self.assertEqual(promo_codes[0].User_ID, self.user.id)
    #     self.assertEqual(promo_codes[0].CODE, 'CODE1')
    #     self.assertEqual(promo_codes[1].EVENT_ID, self.event.ID)
    #     self.assertEqual(promo_codes[1].User_ID, self.user.id)
    #     self.assertEqual(promo_codes[1].CODE, 'CODE2')

    def test_get_apromocode(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('get-promocode', args=[self.discount.ID])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        promo_code = response.data[0]
        self.assertEqual(promo_code['EVENT_ID'], str(self.discount.EVENT_ID))
        self.assertEqual(promo_code['User_ID'], str(self.user.id))
        self.assertEqual(promo_code['CODE'], 'TESTCODE')