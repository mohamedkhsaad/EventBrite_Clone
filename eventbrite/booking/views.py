from django.shortcuts import render
from django.core.mail import send_mail

from eventbrite.email_info import from_email

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters, status

from .serializers import TicketSerializer, DiscountSerializer
from event.serializers import eventSerializer
# models
from .models import Ticket,Discount
from event.models import event as Event
from user.models import User

from django.http import Http404



# TEMP: ticket generics view sets mainly for adding objects into the database
class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]



class discount_list(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
class discount_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


# in-progress
#TODO: configer email service backend
@api_view(['POST'])
def create_ticket(request):
 
    # TODO:
 
    # create a ticket            DONE

    # add it to event tickets    not needed
 
    # add it to user tickets     not needed

    # update event ticket available number  
        # no ticket num attr in event model and it can be calculated without additional attr

    # send confirmation email 

    ticket_serializer = TicketSerializer(data=request.data)
    if ticket_serializer.is_valid():

        ticket_serializer.save()

        # sending confirmation email
        subject = ''
        message = ''
        recipient_list = []

        user = User.objects.get(id = ticket_serializer.data['USER_ID'])
        recipient_list.append(user['email'])

        # send_mail(subject,message,from_email, recipient_list)

        return Response(ticket_serializer.data, status=201)
    return Response(ticket_serializer.errors, status=400)

# DONE 
@api_view(['GET'])
def list_tickets_by_event(request, event_id):

    # get all tickets for this event
    tickets = Ticket.objects.filter(EVENT_ID=event_id)
    serialized_tickets = TicketSerializer(tickets, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_tickets.data)


# TEST after inserting users into the database
@api_view(['GET'])
def list_tickets_by_user(request, user_id):
    # get all tickets for this event
    tickets = Ticket.objects.filter(GUEST_ID=user_id)
    serialized_tickets = TicketSerializer(tickets, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_tickets.data)



#DONE
@api_view(['GET'])
def get_ticket(request,ticket_id):
    # /ticket/{ticket_id}

    try:
        print(ticket_id)
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404

    serialized_ticket = TicketSerializer(ticket, many=False)
    return Response(serialized_ticket.data,status=status.HTTP_200_OK)


# check
@api_view(['GET'])
def check_promo_code(request,event_id):
    # /event?promo_code=SAVE123
    # search an event's promo codes
    try:
        promo_code = request.query_params['promo_code']
    except:
        return Response({'err':'missing promo_code param'},status=status.HTTP_400_BAD_REQUEST)
    
    if not Discount.objects.get(EVENT_ID=event_id,CODE=promo_code):
        return Response({'is_promo_code':False},status=status.HTTP_400_BAD_REQUEST)

    # return ticket object instead
    return Response({'is_promo_code':True},status=status.HTTP_200_OK)
