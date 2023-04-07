"""
This module contains several function based views for the booling app.

function:list_tickets_by_event: A FBV thst Return a list of all tickets for a given event.

function:list_tickets_by_user: A FBV for retrieving list of all tickets for a given user.

function:get_ticket: A FBV that Return a ticket object by ticket ID.

function:check_promo_code: A FBV Check whether a promo code is valid for a given event.

class:discount_list: A view that returns a list of all discounts or creates a new discount.

class:discount_pk: A view that returns a discounts object or update a new discount or delete it.
"""

from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage


from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse

from eventbrite.email_info import from_email

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import TicketSerializer, DiscountSerializer
from event.serializers import eventSerializer

from .models import Ticket,Discount
from event.models import event as Event
from user.models import User

from eventbrite.settings import *







# DONE 
# DONE TESTING
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tickets_by_event(request, event_id):
    """
    Return a list of all tickets for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A list of JSON objects representing the tickets for the given event.
    """
    # get all tickets for this event
    tickets = Ticket.objects.filter(EVENT_ID=event_id)
    serialized_tickets = TicketSerializer(tickets, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_tickets.data)


# DONE TESTING
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tickets_by_user(request, user_id):
    """
    Return a list of all tickets for a given user.

    :param request: HTTP request object.
    :param user_id: User ID.
    :return: A list of JSON objects representing the tickets for the given user.
    """

    tickets = Ticket.objects.filter(GUEST_ID=user_id)
    serialized_tickets = TicketSerializer(tickets, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_tickets.data)



# DONE
# DONE TESTING
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ticket(request,ticket_id):
    # /ticket/{ticket_id}
    """
    Return a ticket object by ticket ID.

    :param request: HTTP request object.
    :param ticket_id: Ticket ID.
    :return: A JSON object representing the ticket for the given ID.
    """
    try:
        # print(ticket_id)
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404

    serialized_ticket = TicketSerializer(ticket, many=False)
    return Response(serialized_ticket.data,status=status.HTTP_200_OK)


# check
# DONE TESTING
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_promo_code(request,event_id):
    """
    Check whether a promo code is valid for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A JSON object indicating whether the promo code is valid.
    """
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




class discount_list(generics.ListCreateAPIView):
    """
    A view class to list and create Discount objects.

    Attributes:
        queryset (QuerySet): A QuerySet of all Discount objects.
        serializer_class (DiscountSerializer): The serializer class for Discount objects.
        authentication_classes (list): A list of authentication classes used for this view.
        permission_classes (list): A list of permission classes used for this view.

    Methods:
        get(self, request, *args, **kwargs):
            Handle HTTP GET request and retrieve a list of Discount objects.
        post(self, request, *args, **kwargs):
            Handle HTTP POST request and create a new Discount object.
    """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class discount_pk(generics.RetrieveUpdateDestroyAPIView):
    """
    A view class to retrieve, update, or delete a Discount object by primary key.

    Attributes:
        queryset (QuerySet): A QuerySet of all Discount objects.
        serializer_class (DiscountSerializer): The serializer class for Discount objects.
        authentication_classes (list): A list of authentication classes used for this view.
        permission_classes (list): A list of permission classes used for this view.

    Methods:
        get(self, request, *args, **kwargs):
            Handle HTTP GET request and retrieve a Discount object by primary key.
        put(self, request, *args, **kwargs):
            Handle HTTP PUT request and update a Discount object by primary key.
        delete(self, request, *args, **kwargs):
            Handle HTTP DELETE request and delete a Discount object by primary key.
    """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# in-progress
#TODO: configer email service backend



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    # print(request.user)
    # TODO:
 
    # create a ticket            DONE

    # send confirmation email    DONE

    ticket_serializer = TicketSerializer(data=request.data)
    if ticket_serializer.is_valid():

        ticket_serializer.save()


        #----------- sending conirmation email ---------
        
        
        # Get the currently logged-in user

        user = request.user
        # print(user.username)


        # Generate a confirmation token
        token = generate_confirmation_token(user.username)

        # Build the confirmation URL
        confirmation_url = request.build_absolute_uri(reverse('create-ticket'))#, args=[token]))

        # Generate a QR code for the confirmation URL using the Google Charts API
        qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
        qr_code_image = requests.get(qr_code_url).content

        # Send the confirmation email
        subject = 'Confirm your email address'
        message = f'Hi {user.username}, please click the link below or scan the QR code to confirm your ticket:\n\n {confirmation_url} \n\n'
        from_email = 'no-reply@example.com'
        recipient_list = [user.email]
        mail = EmailMessage(subject, message, from_email,
                    recipient_list)

        mail.attach(filename='qrcode.png', content=qr_code_image)#,content_type='image/png'
        mail.send()
        # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
        # Render a response



        return Response(ticket_serializer.data, status=201)
    return Response(ticket_serializer.errors, status=400)






# for testing
import requests
@api_view(['GET'])
def send_confirmation_email(request):
    # Get the currently logged-in user

    user = request.user
    # print(user.username)
    # Generate a confirmation token
    token = generate_confirmation_token(user.username)

    # Build the confirmation URL
    confirmation_url = request.build_absolute_uri(reverse('create-ticket'))#, args=[token]))

    # Generate a QR code for the confirmation URL using the Google Charts API
    qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
    qr_code_image = requests.get(qr_code_url).content

    # Send the confirmation email
    subject = 'Confirm your email address'
    message = f'Hi {user.username}, please click the link below or scan the QR code to confirm your ticket:\n\n {confirmation_url} \n\n'
    from_email = 'no-reply@example.com'
    recipient_list = [user.email]
    mail = EmailMessage(subject, message, from_email,
               recipient_list)
    
    mail.attach(filename='qrcode.png', content=qr_code_image)#,content_type='image/png'
    mail.send()
    # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
    # Render a response
    return Response({'status':201}, status=201)

import itsdangerous

def generate_confirmation_token(user):
    serializer = itsdangerous.URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(user)

def confirm_token(token, expiration=3600):
    serializer = itsdangerous.URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, max_age=expiration)
    except:
        return False
    return email








# TEMP: ticket generics view sets mainly for adding objects into the database and testing
class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]