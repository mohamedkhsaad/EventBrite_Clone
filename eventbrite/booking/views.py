"""
This module contains several function based views for the booling app.
function:list_bookings_by_event: A FBV thst Return a list of all bookings for a given event.
function:list_bookings_by_user: A FBV for retrieving list of all bookings for a given user.
function:get_ticket: A FBV that Return a ticket object by ticket ID.
function:check_promo_code: A FBV Check whether a promo code is valid for a given event.
function:create_booking: a FBV that creates a booking object
"""
# class:discount_list: A view that returns a list of all discounts or creates a new discount.
# class:discount_pk: A view that returns a discounts object or update a new discount or delete it.

import itsdangerous
import requests
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from eventbrite.email_info import from_email
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from event.serializers import eventSerializer
from .models import *
from event.models import event as Event
from user.models import User
from eventbrite.settings import *




@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_ticket_classes_by_event(request, event_id):
    """
    Return a list of all ticket class for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A list of JSON objects representing the bookings for the given event.
    """
    # get all bookings for this event
    ticket_classes = TicketClass.objects.filter(EVENT_ID=event_id)
    serialized_Ticket_classes = TicketClassSerializer(ticket_classes, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_Ticket_classes.data)



@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def check_promo_code(request, event_id):
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
        return Response({'err': 'missing promo_code param'}, status=status.HTTP_400_BAD_REQUEST)

    discount = Discount.objects.filter(EVENT_ID=event_id, CODE=promo_code).first()
    if not discount:
        return Response({'is_promo_code': False}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'is_promo_code': True}, status=status.HTTP_200_OK)




# user 
@api_view(['POST'])
def create_order(request):

    """
    recieved data will look like this

        {
            "id" : 1
            "user" : 1
            "event" : 1

            "order_items":
            [
                {
                "ticket_class" : 1,	
                "quantity": 3 
                },
                {
                "ticket_class" : 2,	
                "quantity": 1 
                }
            ],
            full_price : 450
            discount : 200
            fee : 50,
            total: 300,
            is_validated : True
        }

        {
            "order_items":
            [
                {
                "ticket_class" : 1,	
                "quantity": 3 
                },
                {
                "ticket_class" : 2,	
                "quantity": 1 
                }
            ], 
            "promocode" : "DISCOUNT25",
            "event" : 1

        }
    """
    
    order = Order(user = request.user) # create empty order so that orderitem can point to it
    order.save()
    print("-------1--------")

    # Retrieve the request data

    order_items = request.data.get('order_items')
    data = request.data
    data['order'] = order
    print(data)
    

    # Calculate the order
    tickets_costs = [] # a list of ticket cost info object
    subtotal = 0.0
    amount_off = 0.0
    print("--------2-------")

    for item in order_items:
        print(item)
        item['order'] = order.id
        from random import randint
        item['id'] = randint(1,200000)
        print(item)
        order_item_serializer = OrderItemSerializer(data=item)        
        
        if order_item_serializer.is_valid():
            order_item_serializer.save()
            print(order_item_serializer.is_valid())
        

        print("-----3----------")


        ticket_class = order_item_serializer.instance.ticket_class
        quantity = order_item_serializer.instance.quantity
        print(quantity)
        if ticket_class.capacity - ticket_class.quantity_sold < quantity:
            return Response({"details":f"Not enough tickets available for ticket class id {order_item_serializer.instance.ticket_class.id}"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal += ticket_class.price * quantity
        
        ticket_class.quantity_sold += quantity
        ticket_class.save()

    fee = 0
    total = subtotal - amount_off + fee



    event = request.data.get('event')
    if not event:
        return Response({"details":"event wasnt provided"}, status=status.HTTP_400_BAD_REQUEST)


    promocode = request.data.get('promocode')

    discount = Discount.objects.filter(CODE=promocode, EVENT_ID=event).first()
    if not discount:
        return Response({"details":"there isnt any discount with this promocode and event id"}, status=status.HTTP_400_BAD_REQUEST)
    amount_off = float(discount.percent_off)/100 * subtotal

    






    # Create the order
    order_response = {
        'tickets':tickets_costs,
        'full_price' : subtotal,
        'amount_off' : amount_off,
        'fee' : fee,
        'total': total
    }
    order.full_price = subtotal
    # order.amount_off = amount_off
    order.total = total
    order.discount = discount
    order.event_id = event
    order.fee = fee
    order.save()

    return Response(order_response,status=status.HTTP_201_CREATED)



@api_view(['GET'])
def send_confirmation_email(request):
    # Get the currently logged-in user

    user = request.user
    # print(user.username)
    # Generate a confirmation token
    token = generate_confirmation_token(user.username)

    # Build the confirmation URL
    # confirmation_url = request.build_absolute_uri(
    #     reverse('create-booking'))  # , args=[token]))
    confirmation_url = 'google.com'
    # Generate a QR code for the confirmation URL using the Google Charts API
    qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
    qr_code_image = requests.get(qr_code_url).content

    # Send the confirmation email
    subject = 'Confirm your email address'
    message = f'Hi {user.username}, please click the link below or scan the QR code to confirm your booking:\n\n {confirmation_url} \n\n'
    from_email = 'no-reply@example.com'
    recipient_list = [user.email]
    mail = EmailMessage(subject, message, from_email,
                        recipient_list)

    # ,content_type='image/png'
    mail.attach(filename='qrcode.png', content=qr_code_image)
    mail.send()
    # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
    # Render a response
    return Response({'status': 201}, status=201)


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






@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_orders_by_user(request, user_id):
    """
    Return a list of all bookings for a given user.

    :param request: HTTP request object.
    :param user_id: User ID.
    :return: A list of JSON objects representing the bookings for the given user.
    """
    orders = Order.objects.filter(user_id=user_id)
    serialized_orders = OrderSerializer(orders, many=True)
    # return the data as a  list of JSON objects
    return Response(serialized_orders.data)





# @api_view(['POST'])
# def create_order(request):
#     serializer = OrderSerializer(data=request.data)
#     if serializer.is_valid():
#         order = serializer.save()
#         order_items = request.data['items']
#         for item in order_items:
#             item['order'] = order.id
#             item_serializer = OrderItemSerializer(data=item)
#             if item_serializer.is_valid():
#                 item_serializer.save()
#             else:
#                 order.delete()
#                 return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#############################################################  should be get ticket classes
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_booking(request, booking_id):
#     # /booking/{booking_id}
#     """
#     Return a booking object by booking ID.

#     :param request: HTTP request object.
#     :param booking_id: booking ID.
#     :return: A JSON object representing the booking for the given ID.
#     """
#     try:
#         # print(booking_id)
#         booking = Booking.objects.get(id=booking_id)
#     except Booking.DoesNotExist:
#         raise Http404

#     serialized_booking = BookingSerializer(booking, many=False)
#     return Response(serialized_booking.data, status=status.HTTP_200_OK)



# class discount_list(generics.ListCreateAPIView):
#     """
#     A view class to list and create Discount objects.

#     Attributes:
#         queryset (QuerySet): A QuerySet of all Discount objects.
#         serializer_class (DiscountSerializer): The serializer class for Discount objects.
#         authentication_classes (list): A list of authentication classes used for this view.
#         permission_classes (list): A list of permission classes used for this view.

#     Methods:
#         get(self, request, *args, **kwargs):
#             Handle HTTP GET request and retrieve a list of Discount objects.
#         post(self, request, *args, **kwargs):
#             Handle HTTP POST request and create a new Discount object.
#     """
#     queryset = Discount.objects.all()
#     serializer_class = DiscountSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

# class discount_pk(generics.RetrieveUpdateDestroyAPIView):
#     """
#     A view class to retrieve, update, or delete a Discount object by primary key.

#     Attributes:
#         queryset (QuerySet): A QuerySet of all Discount objects.
#         serializer_class (DiscountSerializer): The serializer class for Discount objects.
#         authentication_classes (list): A list of authentication classes used for this view.
#         permission_classes (list): A list of permission classes used for this view.

#     Methods:
#         get(self, request, *args, **kwargs):
#             Handle HTTP GET request and retrieve a Discount object by primary key.
#         put(self, request, *args, **kwargs):
#             Handle HTTP PUT request and update a Discount object by primary key.
#         delete(self, request, *args, **kwargs):
#             Handle HTTP DELETE request and delete a Discount object by primary key.
#     """
#     queryset = Discount.objects.all()
#     serializer_class = DiscountSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]














# in-progress
#TODO: configer email service backend



# def test_send_confirmation_mail(request):

#     # ----------- sending conirmation email ---------

#     # Get the currently logged-in user

#     user = request.user
#     # print(user.username)

#     # Generate a confirmation token
#     token = generate_confirmation_token(user.username)

#     # Build the confirmation URL
#     confirmation_url = request.build_absolute_uri(
#         reverse('create-booking'))  # , args=[token]))

#     # Generate a QR code for the confirmation URL using the Google Charts API
#     qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
#     qr_code_image = requests.get(qr_code_url).content

#     # Send the confirmation email
#     subject = 'Confirm your email address'
#     message = f'Hi {user.username}, please click the link below or scan the QR code to confirm your booking:\n\n {confirmation_url} \n\n'
#     from_email = 'no-reply@example.com'
#     recipient_list = [user.email]
#     mail = EmailMessage(subject, message, from_email,
#                         recipient_list)

#     # ,content_type='image/png'
#     mail.attach(filename='qrcode.png', content=qr_code_image)
#     mail.send()
#     # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
#     # Render a response


# for testing






# pricing functions

