"""
This module contains several view classes for the events app.

class:EventCreateView: A viewset for creating an event instance.

class:AllEventListView: A viewset for retrieving all event instances.

class:EventSearchView: A viewset for searching event instances by title.

class:EventListtype: A viewset for retrieving event instances by type.

class:EventListCategory: A viewset for retrieving event instances by category.

class:EventListSupCategory: A viewset for retrieving event instances by sub-category.

class:EventListVenue: A viewset for retrieving event instances by venue.

class:OnlineEventsAPIView: A viewset for retrieving online event instances.

"""
from django.db.models import Q
import ast


from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from user import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import event
from .serializers import*
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
import json

class EventCreateView(generics.CreateAPIView):
    """
    A viewset for creating an event instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = eventSerializer
    queryset = event.objects.all()


class AllEventListView(APIView):
    """
    A viewset for retrieving all event instances.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        This view should return a list of all the events.
        """

        events = event.objects.all()
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)


class EventSearchView(generics.ListAPIView):
    """
    A viewset for searching event instances by title.
    """
    permission_classes = [IsAuthenticated]
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the title specified in the URL parameter.
        """
        event_name = self.kwargs['event_name']
        return event.objects.filter(Title__icontains=event_name)


class EventListtype(generics.ListAPIView):
    """
    A viewset for retrieving event instances by type.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_type = self.kwargs['event_type']
        return event.objects.filter(type=event_type)


class EventListCategory(generics.ListAPIView):
    """
    A viewset for retrieving event instances by category.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the category specified in the URL parameter.
        """
        event_Category = self.kwargs['event_Category']
        return event.objects.filter(Category=event_Category)


class EventListSupCategory(generics.ListAPIView):
    """
    A viewset for retrieving event instances by sub-category.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the sub-category specified in the URL parameter.
        """
        event_sub_Category = self.kwargs['event_sub_Category']
        return event.objects.filter(sub_Category=event_sub_Category)


class EventListVenue(generics.ListAPIView):
    """
    A viewset for retrieving event instances by venue.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the venue specified in the URL parameter.
        """
        event_venue = self.kwargs['event_venue']
        return event.objects.filter(venue_name=event_venue)


class OnlineEventsAPIView(APIView):
    """
    A viewset for retrieving event which the online is 'true' .
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        This view should return a list of all the online events.
        """
        events = event.objects.filter(online='t')
        serializer = eventSerializer(events, many=True)
        
        return Response(serializer.data)
class EventID(generics.ListAPIView):
    """
    A viewset for retrieving event instances by ID.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the sub-category specified in the URL parameter.
        """
        event_sub_ID = self.kwargs['event_ID']
        return event.objects.filter(ID=event_sub_ID)
    


class UserInterestCreateAPIView(CreateAPIView):
    """
    A viewset for creating an user Interests instance.
    """
    permission_classes = [IsAuthenticated]
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


class UserInterestAPIView(generics.ListAPIView):
    """
    A viewset for retrive an user Interests instance.
    """
    permission_classes = [IsAuthenticated]
    queryset = UserInterest.objects.all()

    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = UserInterestSerializer(queryset, many=True)
        return Response(serializer.data)
    


class UserInterestEventsAPIView(APIView):
    """
    A viewset for retrieving event instances based on user Interests.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve user interests
        user_interests = self.get_user_interests(request.user)

        # Retrieve events related to user interests
        events = self.get_events(user_interests)

        # Serialize data and return response
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)

    def get_user_interests(self, user):
        # Custom logic to retrieve user interests
        return UserInterest.objects.filter(user=user)

    def get_events(self, user_interests):
        # Custom logic to retrieve events related to user interests
        categories = [ui.category_name for ui in user_interests]
        subcategories = [ui.sub_Category for ui in user_interests]
        return event.objects.filter(category_name__in=categories) 
                                    #sub_Category__in=subcategories)

   

