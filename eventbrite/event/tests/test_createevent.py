
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from event.views import*
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import force_authenticate

class EventCreateViewTestCase(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # def test_create_event(self):
    #     image = Image.new('RGB', (100, 100), color='red')
    #     file = BytesIO()
    #     image.save(file, 'png')
    #     file.seek(0)
    #     uploaded_file = SimpleUploadedFile('test.png', file.read(), content_type='image/png')
    #     self.data = {
    #         "ID": "22312",
    #         "User_id": "100",
    #         "Title": "tes1",
    #         "organizer": "ziad",
    #         "Summery": "gggg",
    #         "Description": "music is amazing",
    #         "type": "social",
    #         "category_name": "sporting",
    #         "sub_Category": "football",
    #         "venue_name": "Giza",
    #         "ST_DATE": "2023-04-21",
    #         "END_DATE": "2023-04-21",
    #         "ST_TIME": "05:00:00",
    #         "END_TIME": "06:00:00",
    #         "online": "True",
    #         "CAPACITY": "5000",
    #         "STATUS": "Draft",
    #     }
    #     url = reverse('event-create')
    #     response = self.client.post(url, self.data, format='multipart',follow=True)
    #     # force_authenticate(user=self.user)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(event.objects.count(), 1)
    #     self.assertEqual(event.objects.get().Title, 'tes1')

    def test_create_event_with_invalid_data(self):
        url = reverse('event-create')
        data = data = {
            "ID": "9",
            "User_id": "3",
            "Title": " ",
            "organizer": "test",
            "Description": "test",
            "type": "test",
            "Category": "test",
            "sub_Category": "test",
            "venue_name": "test",
            "CATEGORY_ID": "t5",
            "SUB_CATEGORY_ID": "ss",
            "ST_DATE": "2023-03-23",
            "END_DATE": "2023-04-23",
            "ST_TIME": "05:00:00",
            "END_TIME": "09:00:00",
            "online": "t",
            "CAPACITY": "5000",
            "locationـid": "1",
            "STATUS": "Live"
        }
        response = self.client.post(url, data,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
    
    # def test_get_all_events(self):
    #     response = self.client.get(reverse('event-list-ALL',follow=True))
    #     events = event.objects.all()
    #     serializer = eventSerializer(events, many=True)
    #     # self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)



