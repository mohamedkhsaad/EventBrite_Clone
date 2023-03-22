from rest_framework import routers
from django.urls import path

from .views import TicketList


urlpatterns = [
    path('tickets/', TicketList.as_view(), name='ticket_'),
]