"""
This module contains 2 serializer classes for the user app.

class:userSerializer: A serializer class for creating a new user (Signup).

class:AuthTokenSerializer: A serializer class for the authentication and authorization of the user (login).

"""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
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
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # response = requests.get('https://example.com', verify=False)
        email=validated_data.pop('email')
        password = validated_data.pop('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        username = string.ascii_lowercase
        user = User.objects.create_user(**validated_data, password=password,email=email,
                                       username=''.join(random.choice(username) for i in range(10)) )
        # if user:
        #     raise serializers.ValidationError({'email': 'User with this email already exists.'})
        # else:
        #     user = User.objects.create_user(**validated_data, password=password, email=email,
        #                                         username=''.join(random.choice(username) for i in range(10)))
        # user.save()
        """
        This part is to send a welcoming email to the new user
        """
        # subject = "Welcome to Eventbrite!!"
        # message = "Hello " + user.first_name + "!! \n" + "Welcome to Evenbrite !! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nEventbrite Team"        
        # from_email = EMAIL_HOST_USER
        # to_list = [user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=False)
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
        request=self.context.get('request')
        user=authenticate(
            request=request,
            email=email,
            password=password,
        )
        if not user:
            msg=_('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,code='authorization')
        
        attrs['user']=user
        return attrs


# class EmailCheckSerializer(serializers.Serializer):
#     """
#     Serializer for checking if an email is in the database.
#     """
#     email = serializers.EmailField()

class EmailCheckSerializer(serializers.Serializer):
    # Define a single email field to validate
    email = serializers.EmailField()

    # def validate_email(self, value):
    #     """
    #     Check if the email address is already present in the database.
    #     """
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("Email already exists.")
    #     return value
# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs.get('email')
#         user = get_user_model().objects.filter(email__iexact=email).first()
#         if not user:
#             raise serializers.ValidationError('Invalid email address.')
#         attrs['user'] = user
#         return attrs

#     def send_reset_password_email(self, user):
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)
#         reset_password_link = f"http://eventus.com/user/reset-password/{uid}/{token}/"
#         from_email = EMAIL_HOST_USER

#         send_mail(
#             'Reset your password',
#             f'Please use the following link to reset your password: {reset_password_link}',
#             from_email,
#             [user.email],
#             fail_silently=False,
#         )

#     def save(self):
#         UserModel = get_user_model()
#         email = self.validated_data['email']
#         user = UserModel.objects.get(email=email)
#         self.send_reset_password_email(user)