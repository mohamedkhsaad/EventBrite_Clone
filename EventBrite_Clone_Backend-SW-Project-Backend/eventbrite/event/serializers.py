
from rest_framework import serializers
from .models import *


class eventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    class Meta:
        model = event
        fields = '__all__'


class SearchEventSerializer(serializers.ModelSerializer):
    """
    Serializer for searching the Event model.
    """
    class Meta:
        model = event
        fields = '__all__'
