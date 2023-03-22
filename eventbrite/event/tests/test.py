from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from event.models import event
from event.serializers import eventSerializer

class EventListtypeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.event_type = 'conference'
        event.objects.create(type='meeting', Title='Meeting 1', Description='A meeting.')
        event.objects.create(type='conference', Title='Conference 1', Description='A conference.')
        event.objects.create(type='conference', Title='Conference 2', Description='Another conference.')

    def test_get_event_list_type(self):
        url = reverse('event-list-type', kwargs={'event_type': self.event_type})
        response = self.client.get(url)
        events = event.objects.filter(type=self.event_type)
        serializer = eventSerializer(events, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
