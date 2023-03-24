from django.shortcuts import render

from .models import Ticket,Discount
from .serializers import TicketSerializer, DiscountSerializer
from rest_framework import generics

# Create your views here.

class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

def CheckPromocode(request):
    pass