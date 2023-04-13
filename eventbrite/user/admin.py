from django.contrib import admin
from django.contrib.admin import site

from user.models import*

# Register your models here.
admin.site.register(User)
# admin.site.register(User.admin)
