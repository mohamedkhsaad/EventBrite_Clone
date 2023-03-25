"""
This module contains 2 view classes for the user app.

class:userViewSet: A viewset for creating a new user (Signup).

class:CreateTokenView: A viewset for the authentication and authorization of the user (login).


"""
from .serializers import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import*
from eventbrite.settings import *
# Create your views here.



# @api_view(['POST'])
# def create_user(request):
#     serializer=userSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     else:
#         Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
"""
user model (SIGNUP)
"""
class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for signing up new users.
    """
    serializer_class = userSerializer
    queryset = User.objects.all()



'''
user model (LOGIN)
'''

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