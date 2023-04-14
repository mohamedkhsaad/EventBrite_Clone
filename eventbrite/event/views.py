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
from rest_framework import parsers
from .forms import *
from django.db.models import Q
import ast
from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from user import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from event.models import *
from event.serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
import json
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from django.utils import timezone
from PIL import Image
import os
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import event
from .serializers import eventSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import PageNumberPagination
from booking.models import *
from booking.serializers import *

class EventCreateView(generics.CreateAPIView):
    """
    A viewset for creating an event instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = eventSerializer
    queryset = event.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MyPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        print(self.page)
        return super().get_paginated_response(data)

class AllEventListView(APIView):
    """
    A viewset for retrieving all event instances.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get(self, request, format=None):
        """
        This view should return a paginated list of all the events.
        """
        events = event.objects.all()
        paginator = self.pagination_class()
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = eventSerializer(paginated_events, many=True)
        response = paginator.get_paginated_response(serializer.data)
        response['count'] = paginator.page.paginator.count
        return response


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
        return event.objects.filter(category_name=event_Category)


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
        # sub_Category__in=subcategories)


# class UploadImageView(APIView):
#     def get(self, request):
#         form = ImageForm()
#         return render(request, 'upload_image.html', {'form': form})

#     def post(self, request):
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             return render(request, 'upload_image.html', {'form': form})


# class EventImageCreateView(generics.CreateAPIView):
#     """
#     A viewset for creating an event image instance.
#     """
#     parser_classes = (parsers.MultiPartParser,)

#     def post(self, request, *args, **kwargs):
#         event_id = request.data.get('event_id')
#         try:
#             Event = event.objects.get(ID=event_id)
#         except event.DoesNotExist:
#             return Response({'event_id': f'Event with id {event_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         image_file = request.FILES.get('image')
#         if not image_file:
#             return Response({'image': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         event.image = image_file
#         event.save()

#         serializer = eventSerializer(event)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class TodayEventsList(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        today = now().date()
        queryset = event.objects.filter(ST_DATE=today)
        return queryset


class WeekendEventsView(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        today = timezone.now().date()
        # Find the date of the upcoming Friday
        friday = today + timezone.timedelta((4 - today.weekday()) % 7)
        # Find the date of the upcoming Saturday
        saturday = friday + timezone.timedelta(1)
        queryset = event.objects.filter(
            Q(ST_DATE__gte=friday) & Q(END_DATE__lte=saturday)
        )
        return queryset


# class UploadImageView(APIView):
#     def get(self, request):
#         form = ImageForm()
#         return render(request, 'upload.html', {'form': form})

#     def post(self, request):
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return render(request, 'eventbrite/templates/event/upload.html.html', {'form': form})

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class TicketCreateAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def post(self, request, event_id):
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)
        
        ticket_data = request.data.copy()
        ticket_data['event'] = Event.ID
        serializer = self.serializer_class(data=ticket_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
