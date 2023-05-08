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
class:EventID: A viewset for retrieving event instances by ID.
class:UserInterestCreateAPIView: A viewset for creating an user Interests instance.
class:UserInterestAPIView: A viewset for retrive an user Interests instance.
class:UserInterestEventsAPIView: A viewset for retrieving event instances based on user Interests.
class:TodayEventsList: A viewset for retrieving event instances for today.
class:WeekendEventsView: A viewset for retrieving event instances for weekend.
class:TicketCreateAPIView: A viewset for create a new ticket for a given event
class:EventTicketPrice: A viewset for retrieve the ticket price for a given event.
class:DraftEventsAPIView: A viewset for retrieving Draft events.

"""
from event.forms import *
from django.db.models import Q
from django.shortcuts import render
from event.serializers import *
from user import *
from user.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from event.models import event
from event.serializers import *
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from booking.models import *
from booking.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from booking.models import event, TicketClass
from booking.serializers import *
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user.authentication import CustomTokenAuthentication
from datetime import date

class EventCreateView(generics.CreateAPIView):
    """
    A viewset for creating an event instance.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    serializer_class = eventSerializer
    queryset = event.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the user field to the authenticated user
        serializer.validated_data['user'] = request.user
        # Set the User_id field to the ID of the authenticated user
        serializer.validated_data['User_id'] = request.user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Add user id to response data
        user_id = request.user.id
        response_data = serializer.data
        if response_data.get('online') == 'True':
            response_data['venue_name'] = ""
        elif response_data.get('online') == 'False' and response_data.get('venue_name') == '':
            return Response({'You have to determine a venue name'})
        # response_data['user_id'] = user_id
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class MyPagination(PageNumberPagination):
    """
    A custom pagination class that extends the PageNumberPagination class.
    It sets the page size to 10 by default and overrides the get_paginated_response method to include some print statements and return the paginated response data.
    """
    page_size = 10

    def get_paginated_response(self, data):
        print(self.page)
        return super().get_paginated_response(data)


class AllEventListView(APIView):
    """
    A viewset for retrieving all event instances.
    """
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomTokenAuthentication]
    pagination_class = MyPagination
    def get(self, request, format=None):
        """
        This view should return a paginated list of all the events.
        """
        # events = event.objects.all()
        today = date.today()
        past_events = event.objects.filter(ST_DATE__lt=today, STATUS='Live')
        for past_event in past_events:
           data = {'STATUS': 'Past'}
           event.objects.filter(ID=past_event.ID).update(**data)
            # past_event.save()
        events = event.objects.filter(STATUS='Live')
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

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the venue specified in the URL parameter.
        """
        event_venue = self.kwargs['event_venue']
        return event.objects.filter(venue_name__icontains=event_venue)


class OnlineEventsAPIView(APIView):
    """
    A viewset for retrieving event which the online is 'true' .
    """

    def get(self, request):
        """
        This view should return a list of all the online events.
        """
        events = event.objects.filter(online='True')
        serializer = eventSerializer(events, many=True)

        return Response(serializer.data)


class EventID(generics.ListAPIView):
    """
    A viewset for retrieving event instances by ID.
    """
    serializer_class = eventSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomTokenAuthentication]

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
    authentication_classes = [CustomTokenAuthentication]
    serializer_class = UserInterestSerializer
    queryset = event.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the user field to the authenticated user
        serializer.validated_data['user'] = request.user
        # Set the User_id field to the ID of the authenticated user
        serializer.validated_data['User_id'] = request.user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Add user id to response data
        user_id = request.user.id
        response_data = serializer.data
        # response_data['user_id'] = user_id
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserInterestAPIView(generics.ListAPIView):
    """
    A viewset for retrive an user Interests instance.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    queryset = UserInterest.objects.all()

    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = UserInterestSerializer(queryset, many=True)
        return Response(serializer.data)


class UserInterestEventsAPIView(APIView):
    """
    A viewset for retrieving event instances based on user Interests.
    """
    """
    This function defines a GET request that retrieves a list of events based on the user's interests. 
    It first checks whether the user is authenticated, and if not, returns a 401 Unauthorized response. 
    If the user is authenticated, it retrieves the user's interests using the get_user_interests method and the events related to those interests using the get_events method. 
    Finally, it serializes the retrieved events using the eventSerializer class and returns the serialized data as a response using the Response class. 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

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

    """
    This function retrieves the interests of a given user. It takes a user object as input, 
    and returns a queryset of UserInterest objects that match the given user. 
    """

    def get_user_interests(self, user):
        # Logic to retrieve user interests
        return UserInterest.objects.filter(user=user)
    """
    This function retrieves events related to a given set of user interests. It takes a queryset of UserInterest objects 
    as input, extracts the category and subcategory names from those objects, and returns a queryset of event objects 
    that belong to those categories. 
    """

    def get_events(self, user_interests):
        # Logic to retrieve events related to user interests
        categories = [ui.category_name for ui in user_interests]
        subcategories = [ui.sub_Category for ui in user_interests]
        return event.objects.filter(category_name__in=categories)
        # sub_Category__in=subcategories)


class TodayEventsList(generics.ListAPIView):
    """
    This class defines a GET request that returns a list of events happening today. 
    It uses the eventSerializer class for serialization. The get_queryset method is used to 
    retrieve the events happening on the current date and returns a queryset containing those events. 
    """
    serializer_class = eventSerializer

    def get_queryset(self):
        today = now().date()
        queryset = event.objects.filter(ST_DATE=today)
        return queryset


class WeekendEventsView(generics.ListAPIView):
    """
    This class defines a GET request that returns a list of events happening on the upcoming weekend. 
    It uses the eventSerializer class for serialization. The get_queryset method is used to retrieve 
    the events happening between Friday and Saturday of the upcoming weekend and returns a queryset containing those events. 
    """
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


class TicketCreateAPIView(generics.CreateAPIView):
    """
    This class defines a POST request to create a new ticket for a given event. It uses the TicketC;assSerializer for serialization 
    and the Ticket model for database queries. The post method first checks if the specified event exists in the database, 
    then adds the event ID to the ticket data and attempts to create a new ticket using the serializer. If the serializer is 
    valid, the new ticket is saved and a success response is returned. Otherwise, an error response is returned with the 
    serializer errors.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    queryset = TicketClass.objects.all()
    serializer_class = TicketClassSerializer

    def post(self, request, event_id):
        """
        A POST request to create a ticket object for a given event ID
        """
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)
        ticket_data = request.data.copy()
        ticket_data['event'] = Event.ID
        ticket_data['event_id'] = Event.ID
        print(Event.ID)
        ticket_data['user'] = request.user
        ticket_data['User_id'] = request.user.id
        
        # Check if the user creating the ticket is the same user who created the event
        if str(request.user.id) != str(Event.User_id):
            return Response({'error': 'You are not authorized to create a ticket for this event.'}, status=HTTP_401_UNAUTHORIZED)

        if ticket_data.get('TICKET_TYPE') == 'Free':
            ticket_data['PRICE'] = 0

        serializer = self.serializer_class(data=ticket_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class EventTicketPrice(APIView):
    """
    This class defines a GET request to retrieve the ticket price for a given event. It uses the event and Ticket models 
    for database queries. The get method first checks if the specified event exists in the database, then retrieves the 
    first ticket object associated with the event ID. If the ticket object exists, the ticket price is returned in a 
    success response. Otherwise, an error response is returned indicating that the ticket was not found.
    """

    def get(self, request, event_id):
        """
        Returns the ticket price for a given event.
        """
        try:
            event_obj = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response(status=404, data={'message': 'Event not found'})

        ticket_obj = TicketClass.objects.filter(event_id=event_obj.ID).first()
        if ticket_obj:
            ticket_price = ticket_obj.PRICE
            return Response(status=200, data={'ticket_price': ticket_price})
        else:
            return Response(status=404, data={'message': 'Ticket not found'})


class FreeTicketEventListView(generics.ListAPIView):
    serializer_class = eventSerializer

    def get_queryset(self):
        return event.objects.filter(ticket_set__TICKET_TYPE='Free').distinct()


from django.core.exceptions import PermissionDenied

class DraftEventsAPIView(APIView):
    """
    A viewset for retrieving Draft events.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request):
        """
        This view should return a list of all the draft events of the creator.
        """
        if not request.user.is_authenticated:
            raise PermissionDenied()

        events = event.objects.filter(STATUS='Draft', user=request.user)
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)


class LiveEventsAPIView(APIView):
    """
    A viewset for retrieving Live events.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    def get(self, request):
        """
        This view should return a list of all the draft events of the creator.
        """
        if not request.user.is_authenticated:
            raise PermissionDenied()

        events = event.objects.filter(STATUS='Live', user=request.user)
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)


# followers
class FollowEventView(APIView):
    """
    A viewset for make the user could follow an event by event ID.
    """

    def get(self, request, event_id):
        Event = get_object_or_404(event, ID=event_id)
        if request.user.is_authenticated:
            EventFollower.objects.get_or_create(user=request.user, ID=Event.ID)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to follow an event.'})


class UserFollowedEvents(APIView):
    """
    A viewset for GET the events that the user follow by the user authentication.
    """

    def get(self, request):
        if request.user.is_authenticated:
            event_followers = request.user.event_followers.all()
            events = [get_object_or_404(event, ID=event_follower.ID)
                      for event_follower in event_followers]
            serializer = eventSerializer(events, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'error', 'message': 'You must be logged in to see followed events.'})


class UserFollowedEventsCount(APIView):
    """
    A viewset for count the events that the user follow by the user authentication.
    """

    def get(self, request):
        if request.user.is_authenticated:
            count = request.user.event_followers.count()
            return Response({'status': 'success', 'count': count})
        else:
            return Response({'status': 'error', 'message': 'You must be logged in to see followed events count.'})


class EventFollowersCount(APIView):
    """
    A viewset for count the users that follow an event by event ID.
    """
    serializer_class = EventFollowerSerializer

    def get(self, request, event_id):
        try:
            event_followers = EventFollower.objects.filter(ID=event_id)
            count = event_followers.count()
            return Response({'status': 'success', 'count': count})
        except event.DoesNotExist:
            return Response({'status': 'error', 'message': 'Event does not exist.'})


class UnfollowEventView(APIView):
    """
    A viewset for unfollow an event by event ID.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def delete(self, request, event_id):
        event_follower = get_object_or_404(
            EventFollower, user=request.user, ID=event_id)
        num_deleted, _ = event_follower.__class__.objects.filter(
            user=request.user, ID=event_id).delete()
        if num_deleted > 0:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Could not unfollow event.'})
# likes


class LikeEventView(APIView):
    """
    A viewset for make the user could like an event by event ID.
    """

    def get(self, request, event_id):
        Event = get_object_or_404(event, ID=event_id)
        if request.user.is_authenticated:
            Eventlikes.objects.get_or_create(user=request.user, ID=Event.ID)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to follow an event.'})


class UserLikedEvents(APIView):
    """
    A viewset for GET the events that the user liked by the user authentication.
    """

    def get(self, request):
        if request.user.is_authenticated:
            event_Likes = request.user.event_Likes.all()
            events = [get_object_or_404(event, ID=event_like.ID)
                      for event_like in event_Likes]
            serializer = eventSerializer(events, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'error', 'message': 'You must be logged in to see followed events.'})


class UserLikedEventsCount(APIView):
    """
    A viewset for count the events that the user follow by the user authentication.
    """

    def get(self, request):
        if request.user.is_authenticated:
            count = request.user.event_Likes.count()
            return Response({'status': 'success', 'count': count})
        else:
            return Response({'status': 'error', 'message': 'You must be logged in to see followed events count.'})


class EventLikesCount(APIView):
    """
    A viewset for count the users that follow an event by event ID.
    """
    serializer_class = EventFollowerSerializer

    def get(self, request, event_id):
        try:
            event_Likes = Eventlikes.objects.filter(ID=event_id)
            count = event_Likes.count()
            return Response({'status': 'success', 'count': count})
        except event.DoesNotExist:
            return Response({'status': 'error', 'message': 'Event does not exist.'})


class UnlikeEventView(APIView):
    """
    A viewset for unlike an event by event ID.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def delete(self, request, event_id):
        event_like = get_object_or_404(
            Eventlikes, user=request.user, ID=event_id)
        num_deleted, _ = event_like.__class__.objects.filter(
            user=request.user, ID=event_id).delete()
        if num_deleted > 0:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Could not unfollow event.'})


# manage attendee:
# from django.core.mail import send_mail

# from rest_framework import serializers
# from booking.models import *

# from booking.serializers import *
# class EventAttendeeView(APIView):
#     def post(self, request, event_id):
#         # Retrieve event and ticket classes
#         ticket_classes = TicketClass.objects.filter(EVENT_ID=event_id)
#         # Determine ticket quantities and calculate total price
#         ticket_quantities = []
#         total_price = 0.0
#         for ticket_class in ticket_classes:
#             quantity = ticket_class.capacity
#             print(quantity)
#             if quantity:
#                 quantity = int(quantity)
#                 if quantity > 0:
#                     total_price += ticket_class.PRICE * quantity
#         # Create order
#         Event = event.objects.get(ID=event_id)
#         order = Order.objects.create(event=Event, full_price=total_price)
#         # Create order items and attendees
#         for i, ticket_class in enumerate(ticket_classes):
#             if i < len(ticket_quantities):
#                 quantity = ticket_quantities[i]
#                 if quantity > 0:
#                     order_item = OrderItem.objects.create(order=order, ticket_class=ticket_class, quantity=quantity, ticket_price=ticket_class.PRICE)
#                     for j in range(quantity):
#                         attendee_data = request.data.get(f'ticket_class_{ticket_class.id}_attendee_{j}')
#                         if attendee_data:
#                             serializer = AttendeeSerializer(data=attendee_data)
#                             serializer.is_valid(raise_exception=True)
#                             attendee = serializer.save()
#                             order_item.attendees.add(attendee)

        # return Response({'message': 'Order placed and invitations sent!'})

        # Send email invitation to attendees
        # for order_item in order.order_items.all():
        #     for attendee in order_item.attendees.all():
        #         send_mail(
        #             f'Invitation to {event.name}',
        #             f'Dear {attendee.first_name},\n\nYou have been invited to attend {event.name}! Please present this email at the event check-in to gain access.\n\nBest regards,\n{event.organizer}',
        #             'noreply@example.com',
        #             [attendee.email],
        #             fail_silently=False,
        #         )

        # Return success response
        # return HttpResponse('Order placed and invitations sent!')

class EventUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def put(self, request, event_id):
        try:
            event_obj = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        if str(request.user.id) != str(event_obj.User_id):
            return Response({'error': 'You are not authorized to update this event.'}, status=HTTP_401_UNAUTHORIZED)
        data = {
            'Title': request.data.get('Title', event_obj.Title),
            'organizer': request.data.get('organizer', event_obj.organizer),
            'Summery': request.data.get('Summery', event_obj.Summery),
            'Description': request.data.get('Description', event_obj.Description),
            'type': request.data.get('type', event_obj.type),
            'category_name': request.data.get('category_name', event_obj.category_name),
            'sub_Category': request.data.get('sub_Category', event_obj.sub_Category),
            'venue_name': request.data.get('venue_name', event_obj.venue_name),
            'ST_DATE': request.data.get('ST_DATE', event_obj.ST_DATE),
            'END_DATE': request.data.get('END_DATE', event_obj.END_DATE),
            'ST_TIME': request.data.get('ST_TIME', event_obj.ST_TIME),
            'END_TIME': request.data.get('END_TIME', event_obj.END_TIME),
            'online': request.data.get('online', event_obj.online),
            'CAPACITY': request.data.get('CAPACITY', event_obj.CAPACITY),
            'STATUS': request.data.get('STATUS', event_obj.STATUS),
            'image': request.data.get('image', event_obj.image),
            'image1': request.data.get('image1', event_obj.image1),
            'image2': request.data.get('image2', event_obj.image2),
            'image3': request.data.get('image3', event_obj.image3),
            'image4': request.data.get('image4', event_obj.image4),
            'image5': request.data.get('image5', event_obj.image5)
        }
        event.objects.filter(ID=event_id).update(**data)
        return Response({'message': 'Event updated successfully'})


class TicketClassUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def put(self, request, TicketClass_id):
        try:
            ticket_class_obj = TicketClass.objects.get(ID=TicketClass_id)
        except TicketClass.DoesNotExist:
            return Response({'error': 'Ticket class does not exist.'}, status=HTTP_404_NOT_FOUND)
        if str(request.user.id) != str(ticket_class_obj.User_id):
            return Response({'error': 'You are not authorized to update this ticket class.'}, status=HTTP_401_UNAUTHORIZED)
        data = {
            'NAME': request.data.get('NAME', ticket_class_obj.NAME),
            'PRICE': request.data.get('PRICE', ticket_class_obj.PRICE),
            'capacity': request.data.get('capacity', ticket_class_obj.capacity),
            'quantity_sold': request.data.get('quantity_sold', ticket_class_obj.quantity_sold),
            'TICKET_TYPE': request.data.get('TICKET_TYPE', ticket_class_obj.TICKET_TYPE),
            'Sales_start': request.data.get('Sales_start', ticket_class_obj.Sales_start),
            'Sales_end': request.data.get('Sales_end', ticket_class_obj.Sales_end),
            'Start_time': request.data.get('Start_time', ticket_class_obj.Start_time),
            'End_time': request.data.get('End_time', ticket_class_obj.End_time),
            'Absorb_fees': request.data.get('Absorb_fees', ticket_class_obj.Absorb_fees)
        }
        TicketClass.objects.filter(ID=TicketClass_id).update(**data)
        return Response({'message': 'Ticket class updated successfully'})


class ALLTicketClassListView(generics.ListAPIView):
    serializer_class = TicketClassSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, event_id):
        try:
            ticket_classes = TicketClass.objects.filter(event_id=event_id)
        except TicketClass.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        for ticket_class in ticket_classes:
            if str(request.user.id) != str(ticket_class.User_id):
                return Response({'error': 'You are not authorized to list these ticket classes.'}, status=HTTP_401_UNAUTHORIZED)
        serializer = TicketClassSerializer(ticket_classes, many=True)
        return Response(serializer.data)


class ATicketClassListView(generics.ListAPIView):
    serializer_class = TicketClassSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, TicketClass_id):
        try:
            ticket_classes = TicketClass.objects.filter(ID=TicketClass_id)
        except TicketClass.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        for ticket_class in ticket_classes:
            if str(request.user.id) != str(ticket_class.User_id):
                return Response({'error': 'You are not authorized to lisgt this ticket class.'}, status=HTTP_401_UNAUTHORIZED)
        serializer = TicketClassSerializer(ticket_classes, many=True)
        return Response(serializer.data)


class DeleteeALLTicketClassView(APIView):
    """
    A viewset for deleting all ticket class for an event by event ID.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def delete(self, request, event_id):
        try:
            ticket_classes = TicketClass.objects.filter(event_id=event_id)
        except TicketClass.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        for ticket_class in ticket_classes:
            if str(request.user.id) != str(ticket_class.User_id):
                return Response({'error': 'You are not authorized to delete these ticket classes.'}, status=HTTP_401_UNAUTHORIZED)
        num_deleted, _ = ticket_classes.delete()
        if num_deleted > 0:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Could not delete ticket class.'})


class DeleteeATicketClassView(APIView):
    """
    A viewset for deleting a ticket class for an event by TicketClass_id.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    def delete(self, request, TicketClass_id):
        try:
            ticket_classes = TicketClass.objects.filter(ID=TicketClass_id)
        except TicketClass.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        for ticket_class in ticket_classes:
            if str(request.user.id) != str(ticket_class.User_id):
                return Response({'error': 'You are not authorized to delete this ticket class.'}, status=HTTP_401_UNAUTHORIZED)
        num_deleted, _ = ticket_classes.delete()
        if num_deleted > 0:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Could not delete ticket class.'})


class DeleteeAnEventClassView(APIView):
    """
    A viewset for deleting a ticket class for an event by TicketClass_id.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    def delete(self, request, event_id):
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=HTTP_404_NOT_FOUND)
        # for EVENT in Event:
        if str(request.user.id) != str(Event.User_id):
            return Response({'error': 'You are not authorized to delete this event.'}, status=HTTP_401_UNAUTHORIZED)
        num_deleted, _ = Event.delete()
        if num_deleted > 0:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Could not delete this event.'})