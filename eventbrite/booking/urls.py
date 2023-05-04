from rest_framework import routers
from django.urls import path

from .views import *

urlpatterns = [

    path('events/<int:event_id>/ticket-classes/', list_ticket_classes_by_event, name='list-bookings-by-event'),


    path('events/<int:event_id>/promocode/',check_promocode, name='check-promocode'),


    path('event/<int:event_id>/orders/', create_order, name='create-order'),


    path('mail/', send_confirmation_email,name='confirm-mail'),
    path('confirm-order/<str:token>/',confirm_order,name='confirm-order'),


    path('user/<int:user_id>/orders/', list_orders_by_user, name='list-orders-by-user'),
    path('order/<int:order_id>/order-items/', list_orderitem_by_order, name='list-order-items-by-order'),

    # path('events/<int:event_id>/discounts',list_discounts_by_event, name='list-discount-by-event'),
    # path('booking_generics/', bookingList.as_view(), name='booking-generics'),
    # path('bookings/<int:booking_id>/',get_booking, name='get-booking'),


    # path('events/<int:event_id>/booking/',create_booking,name='create-booking'),

    # path('discount/', discount_list.as_view(), name='discount-list' ),
    # path('discount/<int:pk>/', discount_pk.as_view(), name='discount-item' ),
    # path('events/<int:event_id>/calculate_order/', calculate_order, name='calculate_order'),


]