"""
This module contains 1 model class for the user app.

class:user: A class that contains all fields concerning the user.

"""
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
import uuid
import secrets


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    """
    This class contains all the user fields
    """
    email = models.EmailField(unique=True,blank=False,null=False)
    first_name = models.CharField(max_length=100,blank=False,null=False)
    last_name = models.CharField(max_length=100,blank=False,null=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False,blank=False,null=False)
    is_active = models.BooleanField(default=False,blank=False,null=False)
    username = models.CharField(unique=False,blank=False,null=False,max_length=150)
    # User_ID = models.IntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     related_name='user_groups'
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     related_name='user_permissions_set'
    # )

    def __str__(self):
        return f"{self.id},{self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class CustomToken(models.Model):
    key = models.CharField(max_length=64, unique=True, blank=True)
    user = models.ForeignKey(User, related_name='custom_tokens', on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'CustomToken'
        verbose_name_plural = 'CustomTokens'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        if not self.email:
            self.email = self.user.email
        return super().save(*args, **kwargs)

# class CustomToken(models.Model):
#     key = models.CharField(max_length=40, unique=True, blank=True)
#     user = models.ForeignKey(User, related_name='custom_tokens', on_delete=models.CASCADE)
#     email = models.EmailField()
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'CustomToken'
#         verbose_name_plural = 'CustomTokens'

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = str(uuid.uuid4())
#         if not self.email:
#             self.email = self.user.email
#         return super().save(*args, **kwargs)