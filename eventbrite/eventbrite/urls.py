"""
URL configuration for eventbrite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from user.views import*
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from event.views import*
from user.views import*
from eventManagment.views import*
urlpatterns = [
    path('api/schema/',SpectacularAPIView.as_view(),name='api-schema'),
    path(
    'api/docs/',
    SpectacularSwaggerView.as_view(url_name='api-schema'),
    name='api-docs',
    ),
    # path('admin/', admin.site.urls),
    # user
    path('user/signup/', userViewSet.as_view({'post': 'create'}), name='signup'),
    path('user/login/', CreateTokenView.as_view(), name='token'),
    path('user/emailcheck/<str:email>/', EmailCheckView.as_view(), name='email-check'),
    path('user/reset-password/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('user/reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('user/reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('user/reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),



    # event
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/search/<str:event_name>', EventSearchView.as_view(), name='event_search'),
    path('events/type/<str:event_type>/', EventListtype.as_view(), name='event-list-by-type'),
    path('events/category/<str:event_Category>/', EventListCategory.as_view(), name='event-list-by-category'),
    path('events/sub_category/<str:event_sub_Category>/', EventListSupCategory.as_view(), name='event-list-by-sub_category'),
    path('events/ALL/', AllEventListView.as_view(), name='event-list-ALL'),
    path('events/online/', OnlineEventsAPIView.as_view(), name='online-events'),
    path('events/venue/<str:event_venue>/', EventListVenue.as_view(), name='event-list-by-venue'),
    path('events/ID/<str:event_ID>/', EventID.as_view(), name='event-list-by-ID'),
    path('events/interests-create/', UserInterestCreateAPIView.as_view(), name='user_interests_create'),
    path('events/for-you/', UserInterestEventsAPIView.as_view(), name='user-interests-events'),


    #event management
    path('eventmanagement/userevents/<int:user_id>', UserListEvents.as_view(), name='user_list_events'),
    path('eventmanagement/UserPastEvents/<int:user_id>', UserListPastEvents.as_view(), name='user_list_past_events'),
    path('eventmanagement/UserUpcomingEvents/<int:user_id>', UserListUpcomingEvents.as_view(), name='user_list_upcoming_events'),

    #booking
    path('booking/',include('booking.urls')),
    path('',include('rest_framework.urls')),
]

