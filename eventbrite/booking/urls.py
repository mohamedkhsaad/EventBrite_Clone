from rest_framework import routers
from django.urls import path

from .views import *

urlpatterns = [

    path('user/<int:user_id>/bookings/', list_bookings_by_user, name='list-bookings-by-user'),
    path('events/<int:event_id>/bookings/', list_bookings_by_event, name='list-bookings-by-event'),

    path('bookings/<int:booking_id>/',get_booking, name='get-booking'),

    path('events/<int:event_id>/promocode/',check_promo_code, name='check-promocode'),



    path('mail/', send_confirmation_email,name='confirm-mail'),
    path('events/<int:event_id>/booking/',create_booking,name='create-booking'),

    # path('events/<int:event_id>/calculate_order/', calculate_order, name='calculate_order'),

    path('orders/', create_order, name='create_order'),
    # path('events/<int:event_id>/discounts',list_discounts_by_event, name='list-discount-by-event'),
    # path('booking_generics/', bookingList.as_view(), name='booking-generics'),



    # path('discount/', discount_list.as_view(), name='discount-list' ),
    # path('discount/<int:pk>/', discount_pk.as_view(), name='discount-item' ),

]