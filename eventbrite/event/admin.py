from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(event)
admin.site.register(Tickets)
admin.site.register(Locations)
admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(Discount)

# admin.site.register(user)
# admin.site.register(Interests)