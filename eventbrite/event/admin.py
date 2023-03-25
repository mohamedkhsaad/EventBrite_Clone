"""
Django admin configuration for the event app.

This module contains the registration of the models in the Django admin site.
"""

from django.contrib import admin
from .models import event, Locations, category, sub_category

# Register the event model in the admin site.
admin.site.register(event)

# Register the Locations model in the admin site.
admin.site.register(Locations)

# Register the category model in the admin site.
admin.site.register(category)

# Register the sub_category model in the admin site.
admin.site.register(sub_category)
