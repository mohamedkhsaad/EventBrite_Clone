
from rest_framework import serializers
from .models import*

class eventSerializer(serializers.ModelSerializer):
    class Meta:
        model=event
        fields = '__all__' 

class SearchEventSerializer(serializers.ModelSerializer):
    class Meta:
        model=event
        fields =  '__all__' 
        

    