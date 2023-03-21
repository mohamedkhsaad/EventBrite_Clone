from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse
from .serializers import*
from rest_framework import generics


from .models import event
# Create your views here.

class EventCreateView(generics.CreateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = eventSerializer
    queryset = event.objects.all()


class EventSearchView(generics.ListAPIView):
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        queryset = event.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(Title=name)
        return queryset
    
class EventList(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_type = self.kwargs['event_type']
        return event.objects.filter(type=event_type)