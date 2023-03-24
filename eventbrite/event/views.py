from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from .serializers import*
from rest_framework import generics
from user import*
from datetime import date
import csv



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


class UserListEvents(generics.ListAPIView):
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        # queryset = event.objects.all()
        # event_name = self.request.query_params.get('event_name')
        # if event_name is not None:
        #     queryset = queryset.filter(Title=event_name)
        # return queryset
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id)

class UserListPastEvents(generics.ListAPIView):
    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        # queryset = event.objects.all()
        # event_name = self.request.query_params.get('event_name')
        # if event_name is not None:
        #     queryset = queryset.filter(Title=event_name)
        # return queryset
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__lt=self.today)

class UserListUpcomingEvents(generics.ListAPIView):
    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        # queryset = event.objects.all()
        # event_name = self.request.query_params.get('event_name')
        # if event_name is not None:
        #     queryset = queryset.filter(Title=event_name)
        # return queryset
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__gt=self.today)
    
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

# def ExportCSV(request, **kwargs):

#     response = HttpResponse(content_type='text/csv')

#     writer = csv.writer(response)
#     writer.writerow(['Title', 'ST_DATE', 'STATUS'])
#     user_id =  kwargs['user_id']
#     for x in event.objects.filter(User_id=user_id).values_list('Title', 'ST_DATE', 'STATUS'):
#         writer.writerow(x)

#     response['Content-Disposition'] = 'attachment; filename="My_Events.csv"'

#     return response


# class user_venue(generics.CreateAPIView):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = eventSerializer
#     # queryset = U.venue_name