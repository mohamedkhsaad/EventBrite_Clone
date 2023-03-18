from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets

from .models import*
# Create your views here.

'''
user model 
'''
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields = '__all__' 
    pass

class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = userSerializer
    queryset = user.objects.all()

'''
user interests model 
'''

class user_interests_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Interests
        fields = '__all__' 
    pass

class user_interests_ViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = user_interests_Serializer
    queryset = Interests.objects.all()