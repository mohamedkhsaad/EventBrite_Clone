"""
This module contains several view classes for the eventmanagement app.
class:UserListEvents: A viewset for retrieving all user events by user id.
class:UserListPastEvents: A viewset for retrieving all user past events by user id.
class:UserListEvents: A viewset for retrieving all user upcoming events by user id.
class:PromoCodeCreateAPIView: A viewser for creating a new promocode for a given event.

"""
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from event.serializers import*
from rest_framework import generics
from user import*
from datetime import date
import csv
from event.models import*
from rest_framework.permissions import IsAuthenticated
from booking.models import *
from booking.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from booking.models import event, TicketClass
from booking.serializers import TicketSerializer
import csv

class UserListEvents(generics.ListAPIView):
    """
    A viewset for retrieving all user events by user id.
    """
    permission_classes = [IsAuthenticated]
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should list all the user events
        for the given user id.
        """
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id)

class UserListPastEvents(generics.ListAPIView):
    """
    A viewset for retrieving all user past events by user id.
    """
    permission_classes = [IsAuthenticated]

    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should list all the user past 
        events for the given user id.
        """
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__lt=self.today)

class UserListUpcomingEvents(generics.ListAPIView):
    """
    A viewset for retrieving all user upcoming events by user id.
    """
    permission_classes = [IsAuthenticated]

    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should list all the user upcoming
        events for the given user id.
        """
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__gt=self.today)
    
class PromoCodeCreateAPIView(generics.CreateAPIView):
    """
    A view that creates a promocode for a specific events given the event id
    """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def post(self, request, event_id):
        """
        a post request to create promocode for an event, and have the option to add a csv file instead of typying the promocode details
        """
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)
        
        PromoCode_Data = request.data.copy()
        PromoCode_Data['event'] = Event.ID

        # Check if a CSV file was uploaded
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                # Add the event ID to each row of data before saving
                row['event'] = Event.ID
                serializer = self.serializer_class(data=row)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Promo codes uploaded successfully.'}, status=HTTP_201_CREATED)
        
        # If no CSV file was uploaded, create a single promo code
        else:
            serializer = self.serializer_class(data=PromoCode_Data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
