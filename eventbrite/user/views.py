from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .models import*
# Create your views here.

'''
user model 
'''
class userSerializer(serializers.ModelSerializer):
    
    # first_name=serializers.CharField(max_length=20)
    # last_name=serializers.CharField(max_length=20)
    # email=serializers.EmailField()
    # password=serializers.CharField(max_length=20)

    # username =serializers.CharField(max_length=20)
    # age =serializers.IntegerField()
    # # BIRTH_DATE=serializers.DateField()
    # # PHONE =serializers.CharField(max_length=20)

    # CITY=serializers.CharField(max_length=20)
    # COUNTRY=serializers.CharField(max_length=20)

    # ADDRESS =serializers.CharField(max_length=20)
    # LOCATION_ID =serializers.IntegerField()
    # DISCOUNT_ID=serializers.IntegerField()
    # INTERESTS_ID=serializers.ListField()
    # EVENT_CREATED=serializers.ListField()
    # TICKETS_ID=serializers.ListField()
    # FOLLOWERS=serializers.ListField()
    class Meta:
        model=User
        fields = ['email','first_name','last_name','password','username'] 
    def create_user(self,validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            F_NAME=validated_data['first_name'],
            L_NAME=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password']
           
            # lname=validated_data['lname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

@api_view(['POST'])
def create_user(request):
    serializer=userSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer,status=status.HTTP_201_CREATED)
        

class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = userSerializer
    queryset = User.objects.all()

# '''               
# user interests model 
# '''

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