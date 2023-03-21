from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import*
# Create your views here.

'''
user model 
'''
class userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'age', 'gender', 'city', 'country']

    def create(self, validated_data):
        email=validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password,username=email)
        user.save()
        return user

# class LoginView(APIView):
#     def post(self, request, format=None):
#         data = request.data
#         email = data.get('email', None)
#         password = data.get('PASSWORD', None)
#         user = authenticate(username=email, password=password)
#         if user is not None:
#             login(request, user)
#             serializer = userSerializer(user)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_user(request):
    serializer=userSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = userSerializer
    queryset = User.objects.all()

'''
user interests model 
'''

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