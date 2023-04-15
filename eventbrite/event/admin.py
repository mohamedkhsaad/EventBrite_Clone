"""
Django admin configuration for the event app.

This module contains the registration of the models in the Django admin site.
"""

from django.contrib import admin
from .models import *

# Register the event model in the admin site.
admin.site.register(event)
admin.site.register(UserInterest)
