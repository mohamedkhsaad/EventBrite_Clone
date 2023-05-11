
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from event.models import event
from eventManagment.models import Publish_Info
from event.serializers import eventSerializer

class EventIDTestCase(APITestCase):
    def setUp(self):
        self.event = event.objects.create(
            ID=1,
            User_id=1,
            Title='Online Event 1',
            organizer='Organizer 1',
            Summery='Summary 1',
            Description='Description 1',
            type='Type 1',
            category_name='Category 1',
            sub_Category='music',
            venue_name='Venue 1',
            ST_DATE='2023-04-15',
            END_DATE='2023-04-15',
            ST_TIME='09:00:00',
            END_TIME='10:00:00',
            online='True',
            CAPACITY=50,
            STATUS='Live',
            image=None
        )
        
        self.publish_info = Publish_Info.objects.create(
            Event_ID=1,
            Event_Status="Public",
            Audience_Link="",
            Audience_Password="",
            Keep_Private=False,
            Publication_Date=None
        )

    def test_retrieve_public_event(self):
        url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = eventSerializer(self.event)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_existing_event(self):
        url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, eventSerializer(self.event).data)

    def test_retrieve_nonexistent_event(self):
        url = reverse('event-list-by-ID', kwargs={'event_ID': 999})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,[])

    # def test_retrieve_private_event_unauthenticated(self):
    #     self.publish_info.Event_Status = 'Private'
    #     self.publish_info.save()
    #     url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
    #     response = self.client.get(url,follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK) # Should return 200 even for private event
    #     self.assertIn('This event is private. Please enter the password to view it.', response.data['detail'])
    #     self.assertIn('link', response.data)

    # def test_retrieve_private_event_authenticated_wrong_password(self):
    #     self.publish_info.Event_Status = 'Private'
    #     self.publish_info.Audience_Password = 'password'
    #     self.publish_info.save()
    #     self.client.force_authenticate(user=None)
    #     url = reverse('event-list-by-ID', kwargs={'event_ID': self.event.ID})
    #     response = self.client.get(url,follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK) # Should return 200 even for private event
    #     self.assertIn('This event is private. Please enter the password to view it.', response.data['detail'])
    #     self.assertIn('link', response.data)
    #     # Accessing the event with wrong password should return 401 Unauthorized
    #     url = response.data['link']
    #     response = self.client.post(url, {'password': 'wrong_password'})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
