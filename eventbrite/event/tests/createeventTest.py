
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase
# from event.models import event
# from event.serializers import eventSerializer
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from event.views import*

# class EventCreateViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='ismail',
#             email='ziad@gmail.com',
#             password='512002',)
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#     def test_create_event(self):
#         url = reverse('event-create')
#         data = data = {
#             "ID": 1,
#             "User_id": 3,
#             "Title": "Test Event",
#             "organizer": "test",
#             "Summery": "test",
#             "Description": "test",
#             "type": "test",
#             "category_name": "test",
#             "sub_Category": "test",
#             "venue_name": "test",
#             "ST_DATE": "2023-03-23",
#             "END_DATE": "2023-04-23",
#             "ST_TIME": "05:00:00",
#             "END_TIME": "09:00:00",
#             "online": "True",
#             "CAPACITY": 5000,
#             "PASSWORD": "512002",
#             "STATUS": "Live",
#             "image": ""
#         }
#         response = self.client.post(url, data, format='json')
#         print(response.data)  # print the response data for debugging

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(event.objects.count(), 1)
#         self.assertEqual(event.objects.get().Title, 'Test Event')

#     def test_create_event_with_invalid_data(self):
#         url = reverse('event-create')
#         data = data = {
#             "ID": "9",
#             "User_id": "3",
#             "Title": " ",
#             "organizer": "test",
#             "Description": "test",
#             "type": "test",
#             "Category": "test",
#             "sub_Category": "test",
#             "venue_name": "test",
#             "CATEGORY_ID": "t5",
#             "SUB_CATEGORY_ID": "ss",
#             "ST_DATE": "2023-03-23",
#             "END_DATE": "2023-04-23",
#             "ST_TIME": "05:00:00",
#             "END_TIME": "09:00:00",
#             "online": "t",
#             "CAPACITY": "5000",
#             "PASSWORD": "512002",
#             "locationـid": "1",
#             "STATUS": "test"
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     # def test_serializer(self):
#     #     event_data = data = {
#     #         "ID": "9",
#     #         "User_id": "3",
#     #         "Title": "test",
#     #         "organizer": "test",
#     #         "Description": "test",
#     #         "type": "test",
#     #         "Category": "test",
#     #         "sub_Category": "test",
#     #         "venue_name": "test",
#     #         "CATEGORY_ID": "5",
#     #         "SUB_CATEGORY_ID": "7",
#     #         "ST_DATE": "2023-03-23",
#     #         "END_DATE": "2023-04-23",
#     #         "ST_TIME": "05:00:00",
#     #         "END_TIME": "09:00:00",
#     #         "online": "t",
#     #         "CAPACITY": "5000",
#     #         "PASSWORD": "512002",
#     #         "locationـid": "1",
#     #         "STATUS": "test"
#     #     }
#     #     event_object = event.objects.create(**event_data)
#     #     serializer_data = eventSerializer(event_object).data
#     #     self.assertEqual(set(serializer_data.keys()), set(['id', "ID",
#     #                                                        "User_id", "Title", "organizer", "Description", "type", "Category",
#     #                                                        "sub_Category", "venue_name", "CATEGORY_ID", "SUB_CATEGORY_ID",
#     #                                                        "ST_DATE", "END_DATE", "ST_TIME", "END_TIME",
#     #                                                        "online", "CAPACITY", "PASSWORD", "locationـid", "STATUS"]))
    
#     # def test_get_all_events(self):
#     #     response = self.client.get(reverse('event-list-ALL'))
#     #     events = event.objects.all()
#     #     serializer = eventSerializer(events, many=True)
#     #     self.assertEqual(response.data, serializer.data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)


#     # def test_get_queryset(self):
#     #     view = EventListtype.as_view()
#     #     url = f'/events/type/{self.event.type}/'
#     #     request = self.factory.get(url)
#     #     request.user = self.user
#     #     response = view(request, event_type=self.event1.type)
#     #     serializer_data = eventSerializer([self.event1], many=True).data
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data, serializer_data)
        

