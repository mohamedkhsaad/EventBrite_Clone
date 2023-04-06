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
    path('user/',include('user.urls')),
    path('user/login/', CreateTokenView.as_view(), name='login'),

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


    #event management
    path('eventmanagement/userevents/<int:user_id>', UserListEvents.as_view(), name='user_list_events'),
    path('eventmanagement/UserPastEvents/<int:user_id>', UserListPastEvents.as_view(), name='user_list_past_events'),
    path('eventmanagement/UserUpcomingEvents/<int:user_id>', UserListUpcomingEvents.as_view(), name='user_list_upcoming_events'),

    #booking
    path('booking/',include('booking.urls')),

    path('',include('rest_framework.urls')),
]

