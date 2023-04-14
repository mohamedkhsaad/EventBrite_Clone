
from rest_framework import serializers
from .models import Ticket,Discount

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        exclude = ['event','id']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Discount
        fields =  '__all__' 
