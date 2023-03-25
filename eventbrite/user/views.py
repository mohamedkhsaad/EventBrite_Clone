from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework import viewsets,status,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import*
from django.core.mail import send_mail,EmailMessage
from eventbrite.settings import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# Create your views here.

'''
user model (SIGNUP)
'''
class userSerializer(serializers.ModelSerializer):
    """ User serializer for the signup """
    password = serializers.CharField(style={'input_type':'password'},
                                    trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'age', 'gender', 'city', 'country']

    def create(self, validated_data):
        email=validated_data.pop('email')
        password = validated_data.pop('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        first_name=validated_data['first_name']
        last_name=validated_data['last_name']
        user = User.objects.create_user(**validated_data, password=password,email=email,username=""+first_name +" "+last_name)
        user.save()

        subject = "Welcome to Eventbrite!!"
        message = "Hello " + user.first_name + "!! \n" + "Welcome to Evenbrite !! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nEventbrite Team"        
        from_email = EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return user



""" api view for the create user function"""
@api_view(['POST'])
def create_User(request):
    serializer=userSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = userSerializer
    queryset = User.objects.all()



'''
user model (LOGIN)
'''
class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth Token """
    email=serializers.EmailField()
    password=serializers.CharField(style={'input_type':'password'},
                                    trim_whitespace=False)
    
    def validate(self,attrs):
        """Validate and authenticate the user"""
        email=attrs.get('email')
        password=attrs.get('password')
        if email is None or password is None:
            raise serializers.ValidationError(
                'Email and password are required to log in.')
        print(email)
        print(password)
        request=self.context.get('request')
        user=authenticate(
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

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class=AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES




'''
user interests model 
'''
# class user_interests_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model=Interests
#         fields = '__all__' 
#     pass

# class user_interests_ViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = user_interests_Serializer
#     queryset = Interests.objects.all()