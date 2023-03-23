from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse
from .serializers import*
from rest_framework import generics
from user import*
from rest_framework.response import Response
from rest_framework.views import APIView

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
        # queryset = event.objects.all()
        # event_name = self.request.query_params.get('event_name')
        # if event_name is not None:
        #     queryset = queryset.filter(Title=event_name)
        # return queryset
        event_name = self.kwargs['event_name']
        return event.objects.filter(Title=event_name)
    
class EventListtype(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_type = self.kwargs['event_type']
        return event.objects.filter(type=event_type)
    
class EventListCategory(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_Category = self.kwargs['event_Category']
        return event.objects.filter(Category=event_Category)
    
class EventListSupCategory(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_sub_Category = self.kwargs['event_sub_Category']
        return event.objects.filter(sub_Category=event_sub_Category)
class EventListVenue(generics.ListAPIView):
    serializer_class = eventSerializer
    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_venue = self.kwargs['event_venue']
        return event.objects.filter(venue_name=event_venue)
    
class ALLEventListAPIView(generics.ListAPIView):
    queryset = event.objects.all()
    serializer_class = eventSerializer    
    


class OnlineEventsAPIView(APIView):
    def get(self, request):
        events = event.objects.filter(online='t')
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)


# class user_venue(generics.CreateAPIView):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = eventSerializer
#     # queryset = U.venue_name


