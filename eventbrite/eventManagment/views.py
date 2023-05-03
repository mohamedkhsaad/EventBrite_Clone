"""
This module contains several view classes for the eventmanagement app.
class:UserListEvents: A viewset for retrieving all user events by user id.
class:UserListPastEvents: A viewset for retrieving all user past events by user id.
class:UserListEvents: A viewset for retrieving all user upcoming events by user id.
class:PromoCodeCreateAPIView: A viewser for creating a new promocode for a given event.

"""
from django.shortcuts import render,redirect
from django.urls import reverse

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


from booking.models import *
from booking.serializers import *

import csv
from eventManagment.models import *
from eventManagment.serializers import Publish_InfoSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.signing import TimestampSigner

from eventbrite.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
from django.core.mail import send_mail, EmailMessage


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

class EventPublishView(generics.CreateAPIView):

    serializer_class = Publish_InfoSerializer
    queryset = Publish_Info.objects.all()
    permission_classes = [IsAuthenticated]
    def validate_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def post(self, request,event_id):
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)
        if Publish_Info.objects.filter(Event_ID=event_id):
            return Response({'error': f'Event with id {event_id} already is published.'}, status=HTTP_400_BAD_REQUEST)
        if request.data.get('Event_Status') == 'Private':
            password = request.data.get('Audience_Password')
            if not request.data.get('Audience_Password'):
                return Response({'error': 'Audience Password is required for private events.'}, status=HTTP_400_BAD_REQUEST)
            if validate_password(password):
                return Response({'error': 'Password must contain at least 8 characters, including upper and lower case letters, at least one digit, and at least one special character.'}, status=HTTP_400_BAD_REQUEST)
            if request.data.get('Keep_Private') and request.data.get('Publication_Date'):
                return Response({'error': 'Do not add date, as your event will be kept private'}, status=HTTP_400_BAD_REQUEST)
            if not request.data.get('Keep_Private') and not request.data.get('Publication_Date'):
                return Response({'error': 'Please Provide a Publish Date.'}, status=HTTP_400_BAD_REQUEST)
        
        Publish_Data = request.data.copy()
        Publish_Data['Event_ID'] = event_id
        serializer = self.serializer_class(data=Publish_Data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_msgs = []
            for field, errors in errors.items():
                error_msgs.append(f"{field}: {', '.join(errors)}")
            return Response({'error': error_msgs, 'data': request.data}, status=HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def add_attendee(request,event_id):

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
            "first_name" : "ahmed",
            "last_name" : "hamed",
            "email" : "ahmedhamed@gmail.com"
        }
    
    """
    print("====== add attendee ======")
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')


    user = User.objects.filter(first_name=first_name, last_name=last_name, email=email).first()
    if bool(user) == True:
        print("user already exist")

        data = request.data
        data["user_id"] = user.id
        print(data)
        # redirect to create order 
        url = reverse("create-order",kwargs={'event_id': event_id})
        print(url)
        response = Response(data, status=status.HTTP_302_FOUND)
        response['Location'] = url
        return response
        # return redirect(to = reverse("create-order",args=[event_id]),data=data)   


    return Response(data={"l":"l"},status=status.HTTP_200_OK)
    # get data  
    # check if user exist if not create a user
    # redirect to create order



@api_view(['POST'])
def add_attendee(request,event_id):

    """
    this allows the organizer to add attendee if user doesnt exist it will be created

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
            "first_name" : "ahmed",
            "last_name" : "hamed",
            "email" : "ahmedhamed@gmail.com"
        }
    """
    print("====== add attendee ======")
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')


    user = User.objects.filter(first_name=first_name, last_name=last_name, email=email).first()
    if bool(user) == False:
        print("you should create user")
        data = request.data
        data["password"] = generate_password()
        user_serializer = userSerializer(data = request.data)
        if not user_serializer.is_valid():
            print(user_serializer.error_messages)
        print(user_serializer.is_valid())
        user_serializer.save()
        print(user_serializer.instance)
        user = user_serializer.instance
    print("user already exist")
            


    order = Order(user_id = user.id) # create empty order so that orderitem can point to it
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
        
        if ticket_class.capacity - ticket_class.quantity_sold < quantity:
            order.delete()
            # order_item.delete()
            return Response({"details":f"Not enough tickets available for ticket class id {order_item_serializer.instance.ticket_class_id}"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal += ticket_class.PRICE * quantity
        
        ticket_class.quantity_sold += quantity
        # ticket_class.save()





    if not event.objects.filter(ID = event_id):
        return Response({"details":"no event exist with this ID"}, status=status.HTTP_400_BAD_REQUEST)



    fee = 0
    total = subtotal + fee






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
    order.save()

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
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_orders_by_event(request, event_id):
    """
    Return a list of all orders for a given user.

    :param request: HTTP request object.
    :param user_id: User ID.
    :return: A list of JSON objects representing the bookings for the given user.
    """
    orders = Order.objects.filter(event_id=event_id)
    serialized_orders = OrderSerializer(orders, many=True)
    return Response(serialized_orders.data)
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_orderitem_by_event(request, event_id):
    """

    """
    order_items = OrderItem.objects.filter(event_id=event_id)
    serialized_orderitems = OrderItemSerializer(order_items, many=True)
    return Response(serialized_orderitems.data)

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_orderitem_by_order(request, order_id):
    """

    """
    order_items = OrderItem.objects.filter(order_id=order_id)
    serialized_orderitems = OrderItemSerializer(order_items, many=True)
    return Response(serialized_orderitems.data)



# def ssssssss
#     orders = Order.objects.filter(event_id=event_id)
#     serialized_orders = OrderSerializer(orders, many=True)
#     orders = serialized_orders.data
#     orders[0].id

#     for order in orders:
#         order_items = OrderItem.objects.filter(order_id=order_id)
#         serialized_orderitems = OrderItemSerializer(order_items, many=True)
#         return Response(serialized_orderitems.data)


import random
import string

def generate_password(length=8):
    """Generate a random password of specified length"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password