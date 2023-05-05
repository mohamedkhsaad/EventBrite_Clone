"""
This module contains 2 view classes for the user app.

class:userViewSet: A viewset for creating a new user (Signup).

class:CreateTokenView: A viewset for the authentication and authorization of the user (login).

class:EmailCheckView: A viewset to cheack the emeil
"""
from .serializers import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import *
from eventbrite.settings import *
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view


"""
user model (SIGNUP)
"""
class userViewSet(viewsets.ModelViewSet):
    """
    A viewset for signing up new users.
    """
    serializer_class = userSerializer
    queryset = User.objects.all()
'''
user model (LOGIN)
'''
from rest_framework.status import HTTP_400_BAD_REQUEST


class CustomTokenLoginView(APIView):  
    serializer_class=AuthTokenSerializer
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
            custom_token = CustomToken.objects.create(user=user)
            user_id = user.id
            response_data = {
            'id':user_id,
            'email': user.email,
            'token': custom_token.key 
            }
            user = authenticate(
            request=request,
            email=email,
            password=password,
            )
            # if not user:
            #     msg = _('Unable to authenticate with provided credentials')
            #     raise serializers.ValidationError(msg, code='authorization')
            return Response(response_data, status=status.HTTP_200_OK) 
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




'''
user model (EMAIL CHECK)
'''
user_ = get_user_model()
class EmailCheckView(APIView):
    def get(self, request, email):
        try:
            user = user_.objects.get(email=email)
        except user_.DoesNotExist:
            return JsonResponse({'email_exists': False})
        else:
            return JsonResponse({'email_exists': True})


'''
user model reset password
'''
class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
                return JsonResponse({'email_exists': False})
            if user is not None:
                # Generate a one-time use token for the user's email address
                u_email = urlsafe_base64_encode(force_bytes(user.email))
                token = default_token_generator.make_token(user)
                print(u_email)
                print(token)

                # Construct the reset URL for the user
                reset_url = reverse_lazy('password_reset_check', args={'u_email': u_email, 'token': token})
                # print(uid)
                # print(token)

                # Send the password reset email to the user
                send_mail(
                    'Password reset for your My App account',
                    'Please click the following link to reset your password: ' + reset_url,
                    'noreply@myapp.com',
                    [user.email],
                    fail_silently=False,
                )
                
        # Redirect to the password reset done page
        return HttpResponseRedirect(self.success_url)




class CustomPasswordResetCheckView(APIView):
    serializer_class = PasswordResetQuerySerializer
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        u_email = request.data.get('user_email')
        token = request.data.get('token')

        try:
            u_email = str(urlsafe_base64_decode(u_email), encoding='utf-8', errors='strict')
            user = User.objects.get(email=u_email)
        
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response({'u_email': u_email})
        else:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            msg = _("Unable to find the user's acount with the provided data")
            raise serializers.ValidationError(msg)
        

class CustomPasswordResetConfirmView(APIView):
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['user_email'])
        
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg)
    
        User.objects.filter(email=serializer.validated_data['user_email']).update(password=make_password(serializer.validated_data['password']))
        
        return Response({'detail': 'Password reset successfully.'})


class EmailVerificationQueryView(APIView):
    serializer_class = EmailVerificationQuerySerializer
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u_email = request.data.get('user_email')
        token = request.data.get('token')

        try:
            u_email = str(urlsafe_base64_decode(u_email), encoding='utf-8', errors='strict')
            user = User.objects.get(email=u_email)
           
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and default_token_generator.check_token(user, token):
            User.objects.filter(email=u_email).update(is_active=True)
            return Response({'u_email': u_email})
        else:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            msg = _("Unable to activate the user's acount with the provided data")
            raise serializers.ValidationError(msg)
        

@api_view(['GET'])
def get_user_by_id(request,user_id):
    print("=======")
    print(user_id)
    user = User.objects.get(id=user_id)
    user_serializer = userSerializer(user)
    data = user_serializer.data
    del data['password']
    return Response(data,status=status.HTTP_200_OK)