
# imports
from rest_framework import serializers
from .models import *
from user.serializers import *
from rest_framework import generics, status, request
from rest_framework.response import Response


class eventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_user_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id
        return None

    class Meta:
        model = event
        exclude = ['id']

    def to_representation(self, instance):
        if instance is None:
            return {}
        data = super().to_representation(instance)
        data['Title'] = instance.Title or ''
        return data

    
    add_image_fields(5)


class SearchEventSerializer(serializers.ModelSerializer):
    """
    Serializer for searching the Event model.
    """
    class Meta:
        model = event
        fields = '__all__'


class UserInterestSerializer(serializers.ModelSerializer):
    """
    Serializer for UserInterest model.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_user_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id
        return None

    class Meta:
        model = UserInterest
        fields = '__all__'


class EventFollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the EventFollower model.
    """
    class Meta:
        model = EventFollower
        fields = '__all__'


class EventLikesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Eventlikes model.
    """
    class Meta:
        model = Eventlikes
        fields = '__all__'
