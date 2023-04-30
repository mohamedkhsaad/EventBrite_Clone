from django.db import models
from event.models import *
from bson import ObjectId
# TODO: you have 2 id attributes

class TicketClass(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.FloatField()

    # Number of this Ticket Class available for sale.
    capacity = models.IntegerField()
    # Number of this Ticket Class that has previously been sold
    quantity_sold = models.IntegerField()

    ticket_type_choice = (
        ('Free', 'Free'),
        ('Paid', 'Paind'),
        ('Donation', 'Donation'),
    )
    ticket_type = models.CharField(max_length=10, choices=ticket_type_choice)

    # Sales_start = models.DateField()
    # Sales_end = models.DateField()
    # Start_time = models.DateTimeField()
    # End_time = models.DateTimeField()

    absorb_fees_choices = (
        ('t', 'true'),
        ('f', 'false')
    )
    Absorb_fees = models.CharField(max_length=1, choices=absorb_fees_choices)


class Discount(models.Model):
    ID = models.IntegerField()
    EVENT_ID = models.IntegerField(default=11111)  # should be primary key
    percent_off = models.CharField(max_length=20)
    CODE = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    Quantity_available = models.IntegerField()
    User_ID = models.IntegerField()


        

class Order(models.Model):
    # id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)

    # ticket_classes = models.ManyToManyField(TicketClass, through='OrderItem', related_name='orders')
    
    full_price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,null=True)

    # date_created = models.DateTimeField(auto_now_add=True)

    is_validated = models.BooleanField(default=False)


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    currency = models.CharField(default='USD', max_length=10)


"""
ticket cost object
{
    ticket_class_id : 1,	
    quantity: 3,
    price: 20,
    currency: usd 
}
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)

    ticket_classes = models.ManyToManyField(TicketClass, through='OrderItem', related_name='orders')
    
    full_price = models.DecimalField(max_digits=8, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    date_created = models.DateTimeField(auto_now_add=True)

    is_validated = models.BooleanField(default=False)
order cost object
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


get object list
cost request object list
{
    tickets_quantities:
        [
        {
            ticket_class_id : 1,
            quantity : 2  
        },
        {
            ticket_class_id : 3,
            quantity : 1  
        },
        ]
    promocode : SAVE50
}


for a django rest project write necessery models, serializers and FBV for this case:
if the request should look like this:
[
    {
        ticket_class_id : 1,
        quantity : 2  
    },
    {
        ticket_class_id : 3,
        quantity : 1  
    },
]

and the response should look like this : 
# order cost object
{
   tickets:
     [
        {
        ticket_class_id : 1,	
        quantity: 3,
        price: 20,
        currency: usd 
        },
        {
        ticket_class_id : 2,	
        quantity: 1,
        price: 45,
        currency: usd 
        }
    ],
    promocode : SAVE50,
    fee : 50,
    total: 300
}


note that ticketclass is :
class TicketClass(models.Model):
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    ID = models.IntegerField()
    NAME = models.CharField(max_length=20)
    PRICE = models.FloatField()
    EVENT_ID = models.IntegerField()

    # Number of this Ticket Class available for sale.
    capacity = models.IntegerField()
    # Number of this Ticket Class that has previously been sold
    quantity_sold = models.IntegerField()

    TICKET_TYPE_CHOICES = (
        ('Free', 'Free'),
        ('Paid', 'Paind'),
        ('Donation', 'Donation'),
    )
    TICKET_TYPE = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)

    Sales_start = models.DateField()
    Sales_end = models.DateField()
    Start_time = models.DateTimeField()
    End_time = models.DateTimeField()

    ABSORB_FEES_CHOICES = (
        ('t', 'true'),
        ('f', 'false')
    )
    Absorb_fees = models.CharField(max_length=1, choices=ABSORB_FEES_CHOICES)


"""