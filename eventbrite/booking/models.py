from django.db import models
from event.models import *
from bson import ObjectId
# TODO: you have 2 id attributes


class TicketClass(models.Model):
    # id = models.IntegerField(primary_key=True)

    ID = models.IntegerField(default=generate_unique_id,unique=True)

    event = models.ForeignKey(event, on_delete=models.CASCADE)
    EVENT_ID = models.IntegerField()

    User_id = models.IntegerField(blank=True, null=True)

    NAME = models.CharField(max_length=20,blank=True,null=True)
    PRICE = models.FloatField()

    capacity = models.IntegerField()# Number of this Ticket Class available for sale.
    quantity_sold = models.IntegerField()# Number of this Ticket Class items that has been sold so far

    TICKET_TYPE_CHOICES = (
        ('Free', 'Free'),
        ('Paid', 'Paid'),
        ('Donation', 'Donation'),
    )
    TICKET_TYPE = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES,blank=True,null=True)
    Sales_start = models.DateField()
    Sales_end = models.DateField()
    Start_time = models.DateTimeField()
    End_time = models.DateTimeField()
    ABSORB_FEES_CHOICES = (
        ('True', 'True'),
        ('False', 'False')
    )
    Absorb_fees = models.CharField(max_length=5, choices=ABSORB_FEES_CHOICES)
    
class Discount(models.Model):
    ID = models.IntegerField(default=generate_unique_id,unique=True)
    EVENT_ID = models.IntegerField(default=11111)  # should be primary key
    percent_off = models.IntegerField()
    CODE = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    Quantity_available = models.IntegerField()
    User_ID = models.IntegerField()

        

class Order(models.Model):
    # id = models.IntegerField(primary_key=True)
    ID = models.IntegerField(default=generate_unique_id,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)
    # ticket_classes = models.ManyToManyField(TicketClass, through='OrderItem', related_name='orders')
    full_price = models.FloatField(null=True)
    fee = models.FloatField(null=True)
    total = models.FloatField(null=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    ID = models.IntegerField(default=generate_unique_id,unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ticket_price = models.FloatField(null=True)
    currency = models.CharField(default='USD', max_length=10)