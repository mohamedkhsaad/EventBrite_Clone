from django.db import models
from event.models import *

# TODO: you have 2 id attributes


class Ticket(models.Model):
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    ID = models.IntegerField()
    NAME = models.CharField(max_length=20)
    PRICE = models.FloatField()
    EVENT_ID = models.IntegerField()
    GUEST_ID = models.IntegerField()
    TICKET_NUM = models.IntegerField()
    TICKET_TYPE_CHOICES = (
        ('Free', 'Free'),
        ('VIP', 'VIP'),
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


class Discount(models.Model):
    ID = models.IntegerField()
    EVENT_ID = models.IntegerField(default=11111)  # should be primary key
    percent_off = models.CharField(max_length=20)
    CODE = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    Quantity_available = models.IntegerField()
    User_ID = models.IntegerField()
