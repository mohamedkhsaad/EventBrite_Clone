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
from rest_framework.authtoken.models import Token



from django.urls import reverse
from django.core.signing import TimestampSigner

from eventbrite.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD




@api_view(['GET'])
def list_ticket_classes_by_event(request, event_id):
    """
    Return a list of all ticket class for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A list of JSON objects representing the bookings for the given event.
    """

    
    # get all bookings for this event
    ticket_classes = TicketClass.objects.filter(event_id=event_id)
    serialized_Ticket_classes = TicketClassSerializer(ticket_classes, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_Ticket_classes.data)



@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def check_promocode(request, event_id):
    """
    Check whether a promo code is valid for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A JSON object indicating whether the promo code is valid.
    """
    # /event?promocode=SAVE123
    # search an event's promo codes

    try:
        promocode = request.query_params['promocode']
    except:
        return Response({'err': 'missing promocode param'}, status=status.HTTP_400_BAD_REQUEST)

    discount = Discount.objects.filter(EVENT_ID=event_id, CODE=promocode).first()
    if not discount:
        return Response({'is_promocode': False}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'is_promocode': True}, status=status.HTTP_200_OK)





# fees 
@api_view(['POST'])
def create_order(request,event_id):

    """
    request data should look like this

        {
            "order_items":
            [
                {
                "ticket_class_id" : 1,	
                "quantity": 3 
                },
                {
                "ticket_class_id" : 2,	
                "quantity": 1 
                }
            ], 
            "promocode" : "DISCOUNT25" // optional
            "user_id" : 1 // optional

        }
    """
    # handle promocode
    promocode = request.data.get('promocode')
    if promocode:
        discount = Discount.objects.filter(CODE=promocode, EVENT_ID=event_id).first()
        if not discount:
            
            return Response({"details":"there isnt any discount with this promocode and event id"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data.get('user_id')
    if not user_id:
        user_id = request.user.id
        print( "user_id was got from the request ")

    order = Order(user_id = request.user.id) # create empty order so that orderitem can point to it
    order.save()
    print("-------1--------")

    # Retrieve the request data
  
    order_items = request.data.get('order_items')
    data = request.data
    print(data)
    if not order_items:
        return Response({"details":"""sent data should look like this {
            "order_items":
            [
                {
                "ticket_class_id" : 1,	
                "quantity": 3 
                },
                {
                "ticket_class_id" : 2,	
                "quantity": 1 
                }
            ], 
            "promocode" : "DISCOUNT25"

        }"""}, status=status.HTTP_400_BAD_REQUEST)

    # data['order_id'] = order.ID
    # print(data)


    # for Calculate the order 
    subtotal = 0.0
    amount_off = 0.0
    print("--------2-------")

    for item in order_items:
        
        item['order_id'] = order.ID
        item['ticket_price'] = 999
        item['user_id'] = user_id
        item['event_id'] = event_id

        print(item)



        order_item_serializer = OrderItemSerializer(data=item)               
        if not order_item_serializer.is_valid():
            return Response({"details":f"order item serializer wasnt able to validate the data  {order_item_serializer.error_messages}"}, status=status.HTTP_400_BAD_REQUEST)
        order_item = order_item_serializer.save()
        print(order_item_serializer.is_valid())
        

        print("-----3----------")


        ticket_class = TicketClass.objects.get(ID=order_item_serializer.instance.ticket_class_id)
        print(ticket_class.PRICE)
        quantity = order_item_serializer.instance.quantity
        print(quantity)
        print(ticket_class.capacity)
        print(ticket_class.quantity_sold)
        if int(ticket_class.capacity) - int(ticket_class.quantity_sold) < quantity:
            order.delete()
            # order_item.delete()
            return Response({"details":f"Not enough tickets available for ticket class id {order_item_serializer.instance.ticket_class_id}"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal += ticket_class.PRICE * quantity
        
        ticket_class.quantity_sold += str(quantity)
        # ticket_class.save()





    if not event.objects.filter(ID = event_id):
        return Response({"details":"no event exist with this ID"}, status=status.HTTP_400_BAD_REQUEST)

    if promocode:
        order.discount_id = discount.ID
        amount_off = float(discount.percent_off)/100 * subtotal

    fee = 0
    total = subtotal - amount_off + fee






    # Create the order
    order_response = {
        'tickets':order_items,
        'full_price' : subtotal,
        'amount_off' : amount_off,
        'fee' : fee,
        'total': total
    }
    order.full_price = subtotal
    order.amount_off = amount_off
    order.total = total
    order.event_id = event_id
    order.fee = fee
    # order.save()

    send_confirmation_email(request._request,order)

    return Response(order_response,status=status.HTTP_201_CREATED)


def send_confirmation_email(request,order):

    """ this function should construct the url with a token and send the link by mail to the user """


    print("======confirmation mail=======")
    user = request.user

    # Generate a confirmation token
    signer = TimestampSigner()
    token = signer.sign(str(order.id))
    # token = generate_confirmation_token(order.id)

    print(token)

    confirmation_url = request.build_absolute_uri(reverse('confirm-order', args=[token]))


    print("======1=======")

    # Build the confirmation URL
    # confirmation_url = request.build_absolute_uri(
    #     reverse('create-booking'))  # , args=[token]))
    
    # token, created = Token.objects.get_or_create(user=user)
    # confirmation_url = 'google.com'
    # confirmation_url = f"https://example.com/confirm-email/?token={token.key}"




    # Generate a QR code for the confirmation URL using the Google Charts API
    qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
    qr_code_image = requests.get(qr_code_url).content
    print("======2=======")

    # Send the confirmation email
    subject = 'Confirm your email address'
    message = f'Hi {user.username}, please click the link below or scan the QR code to confirm your booking:\n\n {confirmation_url} \n\n'
    from_email = 'no-reply@example.com'
    recipient_list = [user.email]
    print(recipient_list)
    mail = EmailMessage(subject, message, from_email,
                        recipient_list)
    print(EMAIL_HOST_USER)
    send_mail(subject=subject, message=message,
            from_email=from_email,
            fail_silently=False,
            recipient_list = ["to@example.com"])
    print("======3=======")

    # ,content_type='image/png'
    mail.attach(filename='qrcode.png', content=qr_code_image)
    mail.send()
    # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
    # Render a response
    print("====== end of function =======")

    return Response({'status': 201}, status=201)


@api_view(['GET'])
def confirm_order(request, token):
    print("=-=-=-=-= start confirm order==-=--=---=")

    signer = TimestampSigner()
    try:
        order_id = signer.unsign(token, max_age=86400) # 86400 seconds = 1 day
    except signer.BadSignature:
        return Response({'details':'Invalid token'})

    print("=-=-=-=-= mid confirm order==-=--=---=")
    print(id)
    order = Order.objects.get(id=order_id)
    order.is_validated = True
    order.save()
    print("=-=-=-=-= end confirm order==-=--=---=")

    return Response({"is_validated":True},status=status.HTTP_200_OK)





@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_orders_by_user(request, user_id):
    """
    Return a list of all orders for a given user.

    :param request: HTTP request object.
    :param user_id: User ID.
    :return: A list of JSON objects representing the bookings for the given user.
    """
    orders = Order.objects.filter(user_id=user_id)
    serialized_orders = OrderSerializer(orders, many=True)
    return Response(serialized_orders.data)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_orderitem_by_order(request, order_id):
    """

    """
    order_items = OrderItem.objects.filter(order_id=order_id)
    serialized_orderitems = OrderItemSerializer(order_items, many=True)
    return Response(serialized_orderitems.data)

