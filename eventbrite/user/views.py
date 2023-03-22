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
# Create your views here.

'''
user model (SIGNUP)
'''
class userSerializer(serializers.ModelSerializer):
    """ User serializer for the signup """
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'age', 'gender', 'city', 'country']

    def create(self, validated_data):
        email=validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password,email=email,username="default")
        user.save()
        return user


@api_view(['POST'])
def create_user(request):
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
        user=authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
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