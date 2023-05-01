from rest_framework import serializers
from .models import Publish_Info

class Publish_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish_Info
        fields = '__all__'
