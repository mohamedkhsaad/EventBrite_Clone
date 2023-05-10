# from rest_framework.test import APIClient, APITestCase
# from event.models import event
# from datetime import date
# from rest_framework import status
# from event.serializers import *
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from event.models import event
# from event.serializers import eventSerializer
# from django.contrib.auth import get_user_model
# from datetime import date

# class EventManagementTest(APITestCase):
#     def setUp(self):
#             self.user = get_user_model().objects.create_user(
#                 username='Abdelrhman',
#                 email='Belshahed01@gmail.com',
#                 password='000000',)
#             self.client = APIClient()
#             self.client.force_authenticate(user=self.user)
#             self.user_id = 1190507
#             self.today = date.today()
#             self.start_date = date(2023, 3, 5)
#             self.start_date1 = date(2023, 4, 10)

#             self.event1 = event.objects.create(
#                 ID="1",User_id=self.user_id , Title="Test Event", organizer="test",
#                 Description="test", type="music", category_name="test", sub_Category="test", venue_name="test",
#                 ST_DATE=self.start_date,END_DATE=date(2023, 7, 4), ST_TIME="05:00:00",
#                 END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="000000", STATUS="test")
            
#             self.event2 = event.objects.create(
#                 ID="2", User_id= self.user_id , Title="Test Event", organizer="test",
#                 Description="test", type="food", category_name="test", sub_Category="test", venue_name="test",
#                 ST_DATE=self.start_date1, END_DATE= date(2023, 5, 4), ST_TIME="05:00:00",
#                 END_TIME="09:00:00", online="t", CAPACITY="5000", PASSWORD="000000", STATUS="test")


#     def test_retrieve_all_user_events_by_user_id(self):
#             url = reverse('user_list_events', kwargs={'user_id': self.user_id})
#             response = self.client.get(url, follow=True)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data), 2)
#             event_data1 = response.data[0]
#             event_data2= response.data[1]
#             serializer1 = eventSerializer(self.event1)
#             serializer2 = eventSerializer(self.event2)
#             self.assertEqual(event_data1, serializer1.data)
#             self.assertEqual(event_data2, serializer2.data)

#     def test_retrieve_all_user_past_events_by_user_id(self):
#             url = reverse('user_list_past_events', kwargs={'user_id': self.user_id})
#             response = self.client.get(url, follow=True)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             queryset = event.objects.filter(User_id=self.user_id,ST_DATE__lt=self.today)
#             serializer = eventSerializer(queryset, many=True)
#             event_data = response.data
#             # print(response.data)
#             self.assertEqual(event_data, serializer.data)

            

#     def test_retrieve_all_user_upcoming_events_by_user_id(self):
#             url = reverse('user_list_upcoming_events', kwargs={'user_id': self.user_id})
#             response = self.client.get(url, follow=True)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             queryset = event.objects.filter(User_id=self.user_id).filter(ST_DATE__gt=self.today)
#             serializer = eventSerializer(queryset, many=True)
#             event_data = response.data
#             # print(response.data)
#             self.assertEqual(event_data, serializer.data)


