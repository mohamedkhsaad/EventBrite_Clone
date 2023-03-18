from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets

from .models import*
# Create your views here.

class eventSerializer(serializers.ModelSerializer):
    class Meta:
        model=event
        fields = '__all__' 

    pass
class eventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = eventSerializer
    queryset = event.objects.all()