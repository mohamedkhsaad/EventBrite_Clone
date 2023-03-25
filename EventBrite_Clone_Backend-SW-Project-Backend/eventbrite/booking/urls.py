from rest_framework import routers
from django.urls import path

from .views import TicketList,DiscountList,list_tickets_by_user, list_tickets_by_event,create_ticket, get_ticket, check_promo_code


urlpatterns = [
    path('ticket_generics/', TicketList.as_view(), name='ticket-generics'),
    path('discount_generics/', DiscountList.as_view(), name='discount-generics' ),

    path('tickets/',create_ticket,name='create-ticket'),
    path('tickets/<int:ticket_id>/',get_ticket, name='get-ticket'),
    path('user/<int:user_id>/tickets/', list_tickets_by_user, name='list-tickets-by-user'),
    path('events/<int:event_id>/tickets/', list_tickets_by_event, name='list-tickets-by-event'),
    path('events/<int:event_id>/',check_promo_code, name='check-promocode'),
]