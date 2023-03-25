"""
This module contains several view classes for the eventmanagement app.
class:UserListEvents: A viewset for retrieving all user events by user id.
class:UserListPastEvents: A viewset for retrieving all user past events by user id.
class:UserListEvents: A viewset for retrieving all user upcoming events by user id.
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

class UserListEvents(generics.ListAPIView):
    """
    A viewset for retrieving all user events by user id.
    """
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
    
