from django.shortcuts import render
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from event.serializers import*
from rest_framework import generics
from user import*
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import date
from event.models import event



class UserListEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = event.objects.all()
    serializer_class = eventSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id)

class UserListPastEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__lt=self.today)

class UserListUpcomingEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    today = date.today()
    queryset = event.objects.all()
    serializer_class = eventSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return event.objects.filter(User_id=user_id).filter(ST_DATE__gt=self.today)
    