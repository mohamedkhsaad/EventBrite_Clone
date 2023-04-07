"""
This module contains 2 serializer classes for the user app.

class:userSerializer: A serializer class for creating a new user (Signup).

class:AuthTokenSerializer: A serializer class for the authentication and authorization of the user (login).

"""
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import*
from django.core.mail import send_mail
from eventbrite.settings import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import string
import random
from django.http import HttpResponse
import requests

class userSerializer(serializers.ModelSerializer):
    """
    User serializer for the signup
    """
    password = serializers.CharField(style={'input_type':'password'},
                                    trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'age', 'gender', 'city', 'country']

    def create(self, validated_data):
        # response = requests.get('https://example.com', verify=False)
        email=validated_data.pop('email')
        password = validated_data.pop('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        # first_name=validated_data['first_name']
        # last_name=validated_data['last_name']
        username = string.ascii_lowercase
        user = User.objects.create_user(**validated_data, password=password,email=email,
                                       username=''.join(random.choice(username) for i in range(10)) )
        user.save()
        """
        This part is to send a welcoming email to the new user
        """
        subject = "Welcome to Eventbrite!!"
        message = "Hello " + user.first_name + "!! \n" + "Welcome to Evenbrite !! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nEventbrite Team"        
        from_email = EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ 
    Serializer for the user auth Token
    """
    email=serializers.EmailField()
    password=serializers.CharField(style={'input_type':'password'},
                                    trim_whitespace=False)
    
    def validate(self,attrs):
        """Validate and authenticate the user"""
        email=attrs.get('email')
        password=attrs.get('password')
        print(email)
        print(password)
        request=self.context.get('request')
        user=authenticate(
            request=request,
            
            email=email,
            password=password,
        )
        print(user)
        print(request)
        if not user:
            msg=_('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,code='authorization')
        
        attrs['user']=user
        return attrs


class EmailCheckSerializer(serializers.Serializer):
    """
    Serializer for checking if an email is in the database.
    """
    email = serializers.EmailField()
