from rest_framework import routers
from django.urls import path

from .views import TicketList,discount_list,discount_pk,list_tickets_by_user, list_tickets_by_event,create_ticket, get_ticket, check_promo_code, send_confirmation_email

urlpatterns = [

    path('user/<int:user_id>/tickets/', list_tickets_by_user, name='list-tickets-by-user'),
    path('events/<int:event_id>/tickets/', list_tickets_by_event, name='list-tickets-by-event'),

    path('tickets/<int:ticket_id>/',get_ticket, name='get-ticket'),

    path('events/<int:event_id>/promocode/',check_promo_code, name='check-promocode'),

    path('discount/', discount_list.as_view(), name='discount-list' ),
    path('discount/<int:pk>', discount_pk.as_view(), name='discount-item' ),

     # path('test_Send_confirmation_mail/', send_confirmation_email,name='confirm-mail'),

 

 
    # path('events/<int:event_id>/discounts',list_discounts_by_event, name='list-discount-by-event'),
    # path('ticket_generics/', TicketList.as_view(), name='ticket-generics'),
    # path('tickets/',create_ticket,name='create-ticket'),

]