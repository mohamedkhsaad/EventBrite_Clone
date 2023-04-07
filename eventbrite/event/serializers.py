
from rest_framework import serializers
from .models import *
from user.serializers import *

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


class UserInterestSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    category_name = serializers.CharField(max_length=255)

    class Meta:
        model = UserInterest
        fields = ['id', 'user', 'category_name']
