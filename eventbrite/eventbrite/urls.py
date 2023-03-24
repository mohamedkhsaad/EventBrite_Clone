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

urlpatterns = [
    path('api/schema/',SpectacularAPIView.as_view(),name='api-schema'),
    path(
    'api/docs/',
    SpectacularSwaggerView.as_view(url_name='api-schema'),
    name='api-docs',
    ),
    # path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/search/<str:event_name>', EventSearchView.as_view(), name='event_search'),
    path('events/list_user_events/<int:user_id>', UserListEvents.as_view(), name='user_list_events'),
    path('events/list_user_past_events/<int:user_id>', UserListPastEvents.as_view(), name='user_list_past_events'),
    path('events/list_user_upcoming_events/<int:user_id>', UserListUpcomingEvents.as_view(), name='user_list_upcoming_events'),
    path('events/type/<str:event_type>/', EventListtype.as_view(), name='event-list-by-type'),
    path('events/category/<str:event_Category>/', EventListCategory.as_view(), name='event-list-by-category'),
    path('events/sub_category/<str:event_sub_Category>/', EventListSupCategory.as_view(), name='event-list-by-sub_category'),
    # path('events/export_csv/<int:user_id>', ExportCSV, name='export-csv'),



    path('',include('rest_framework.urls')),
]

