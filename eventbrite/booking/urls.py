from rest_framework import routers
from django.urls import path

from .views import *

urlpatterns = [

    path('events/<int:event_id>/ticket-classes/',
         list_ticket_classes_by_event, name='list-ticket-classes-by-event'),
    path('events/<int:event_id>/promocode/',
         check_promocode, name='check-promocode'),
    path('event/<int:event_id>/orders/', create_order, name='create-order'),
    path('mail/', send_confirmation_email, name='confirm-mail'),
    path('confirm-order/<str:token>/', confirm_order, name='confirm-order'),
    path('user/<int:user_id>/orders/',
         list_orders_by_user, name='list-orders-by-user'),
    path('order/<int:order_id>/order-items/',
         list_orderitem_by_order, name='list-order-items-by-order'),

]
