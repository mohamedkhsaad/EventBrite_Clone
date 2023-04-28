"""
This module contains 2 serializer classes for the user app.
class:userSerializer: A serializer class for creating a new user (Signup).
class:AuthTokenSerializer: A serializer class for the authentication and authorization of the user (login).
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.core.mail import send_mail
from eventbrite.settings import *
# from django.contrib.auth.password_validation import validate_password
import re
from django.core.exceptions import ValidationError
import string
import random
from django.http import HttpResponse
import requests
from django.urls import reverse_lazy


class userSerializer(serializers.ModelSerializer):
    """
    User serializer for the signup
    """
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        username = string.ascii_lowercase
        user = User.objects.create_user(**validated_data, password=password, email=email,
                                        username=''.join(random.choice(username) for i in range(10)))
        user.is_active=False
        
        """
        This part is to send a welcoming email to the new user
        """
        uid = urlsafe_base64_encode(force_bytes(user.email))
        token = default_token_generator.make_token(user)

                # Construct the reset URL for the user
        reset_url = reverse_lazy('verify_mail', args={'uid': uid, 'token': token})
        print(uid)
        print(token)
        

                # Send the password reset email to the user
        send_mail(
            'Password reset for your My App account',
            'Please click the following link to reset your password: ' + reset_url,
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
                )
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ 
    Serializer for the user auth Token
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        users=User.objects.all()
        print(users)
        user = authenticate(
            request=request,
            email=email,
            password=password,
        )
        print(user)
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
       
        return attrs

class EmailVerificationQuerySerializer(serializers.Serializer):
    user_id=serializers.CharField()
    token=serializers.CharField()


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetQuerySerializer(serializers.Serializer):
    user_id=serializers.CharField()
    token=serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    user_id = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return data

def generate_otp():
        """
        Generate a 6-digit OTP.
        """
        return str(random.randint(100000, 999999))



def validate_password(password):
    """
    Validate that the password is strong enough.
    """
    # Check password length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check for uppercase letters
    if not re.search('[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    # Check for lowercase letters
    if not re.search('[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    # Check for digits
    if not re.search('\d', password):
        raise ValidationError("Password must contain at least one digit.")

    # Check for special characters
    if not re.search('[^A-Za-z0-9]', password):
        raise ValidationError("Password must contain at least one special character.")

    return password



from pymongo import MongoClient

def delete_user(email):
    # Set up the MongoDB client
    client = MongoClient('mongodb://localhost:27017/')
    
    # Select the users collection
    db = client['dani']
    users = db['users']
    
    # Delete the user with the given email address
    result = users.delete_one({'email': email})
    
    # Return True if the user was deleted successfully, False otherwise
    return result.deleted_count > 0
