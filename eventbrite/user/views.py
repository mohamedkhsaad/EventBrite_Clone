"""
This module contains view classes for the user app.

class:userViewSet: A viewset for creating a new user (Signup).

class:CustomTokenLoginView: A viewset for the authentication and authorization of the user (login).

class:EmailCheckView: A viewset to check the email

class:CustomPasswordResetView: a viewset to send the user email to change his password.

class:CustomPasswordResetCheckView: a viewset to check the token and the u_email in the user link.    

class:CustomPasswordResetConfirmView: a viewset for the user to change his password.

class:EmailVerificationQueryView: a viewset for the user to verify the token and u_email in the link to verify and activate his account.

function:get_user_by_id: a view function to retrieve the user info by user id
"""
from rest_framework.status import HTTP_400_BAD_REQUEST
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


class CustomTokenLoginView(APIView):
    '''
This is a view class for the user login. User has to verify his email after signup to be able to login
    '''
    serializer_class = AuthTokenSerializer

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
                'id': user_id,
                'email': user.email,
                'token': custom_token.key,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'initials': (user.first_name[0] if user.first_name else '') + (user.last_name[0] if user.last_name else '')

            }
            response_data['initials'] = response_data['initials'].upper()

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
    '''
This is a view class for the user email check. 
It checks if the email entered is in the database or not
    to redirect the user either to the signup or to login.
    '''

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


class CustomPasswordResetView(APIView):
    '''
This is a view class to allow the user to enter his email to reset his password.
If the email doesn't exist in the database it returns a json response that the email doesn't exist.
If the email exists the class sends him an email with his email encrypted in the query with a token. 
    '''
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
                reset_url = reverse_lazy('password_reset_check', args={
                                         'u_email': u_email, 'token': token})
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
    '''
This is a view class to check the link (sent earlier by email) clicked by the user to reset his password.
The class checks the token and the u_email from the query
    '''
    serializer_class = PasswordResetQuerySerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        u_email = request.data.get('user_email')
        token = request.data.get('token')

        try:
            u_email = str(urlsafe_base64_decode(u_email),
                          encoding='utf-8', errors='strict')
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
    '''
This is a view class for the user to reset his password 
and for the frontend to put the email to specify the user to update his password.
    '''
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['user_email'])

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg)

        User.objects.filter(email=serializer.validated_data['user_email']).update(
            password=make_password(serializer.validated_data['password']))

        return Response({'detail': 'Password reset successfully.'})


class EmailVerificationQueryView(APIView):
    '''
This is a view class for the user to verify his email to activate his account
by clicking the link sent to him by mail right after signing up.
    '''
    serializer_class = EmailVerificationQuerySerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u_email = request.data.get('user_email')
        token = request.data.get('token')

        try:
            u_email = str(urlsafe_base64_decode(u_email),
                          encoding='utf-8', errors='strict')
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
def get_user_by_id(request, user_id):
    '''
This is a function to retrieve the user info by the user id. (Used in dashboard).
    '''
    try:
        user = User.objects.get(id=(user_id))
    except User.DoesNotExist:
        user = None
        return JsonResponse({'user_exists': False})
    user_serializer = userSerializer(user)
    data = user_serializer.data
    # del data['password']
    return Response(data, status=status.HTTP_200_OK)
