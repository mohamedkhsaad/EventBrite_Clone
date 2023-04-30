from django.db import models
from event.models import *
from event.models import *
# TODO: you have 2 id attributes


class TicketClass(models.Model):
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    ID = models.IntegerField(default=generate_unique_id,unique=True)
    EVENT_ID = models.IntegerField()
    User_id = models.IntegerField(blank=True, null=True)
    NAME = models.CharField(max_length=20,blank=True,null=True)
    PRICE = models.FloatField()
    # GUEST_ID = models.IntegerField(null=True)
    capacity = models.IntegerField()
    quantity_sold = models.IntegerField()
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
    full_price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

class OrderItem(models.Model):
    # id = models.IntegerField(primary_key=True)
    ID = models.IntegerField(default=generate_unique_id,unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    ticket_class = models.ForeignKey(TicketClass, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    currency = models.CharField(default='USD', max_length=10)