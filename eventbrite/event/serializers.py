
from rest_framework import serializers
from .models import *
from user.serializers import *
from rest_framework import generics, status, request
from rest_framework.response import Response


class eventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    # image, image2, image3,image4 = tuple(serializers.ImageField(max_length=None,use_url=True,required=False, allow_null=True)for i in range(4))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user_id = serializers.SerializerMethodField()
    def get_user_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id
        return None
    class Meta:
        model = event
        fields = '__all__'

        # exclude = ['U]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance is not None:
            data['Title'] = instance.Title or ''
        return data


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



class EventFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFollower
        fields = '__all__'


class EventLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventlikes
        fields = '__all__'


