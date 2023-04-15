
from rest_framework import serializers
from .models import *
from user.serializers import *
from rest_framework import generics, status, request
from rest_framework.response import Response


class eventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = event
        exclude = ['user']


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
    user = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all())
    category_name = serializers.CharField(max_length=255)
    sub_Category = serializers.ListField(
        child=serializers.CharField(max_length=255), allow_empty=True)

    class Meta:
        model = UserInterest
        fields = ['id', 'user', 'category_name', 'sub_Category']
