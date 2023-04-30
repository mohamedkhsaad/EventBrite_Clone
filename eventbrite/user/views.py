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
# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for user"""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         user_id = user.id
#         token, _ = Token.objects.get_or_create(user=user)
#         # Create response data
#         response_data = {
#             'id': user_id,
#             'email': user.email,
#             'password': request.data.get('password'),
#             'token': token.key,
#         }
#         return Response(response_data)

#     def is_token_valid(self, token_key):
#         try:
#             token = Token.objects.get(key=token_key)
#             return True
#         except Token.DoesNotExist:
#             return False

#     def get(self, request, *args, **kwargs):
#         token_key = request.GET.get('token', None)
#         if not token_key:
#             return Response({'error': 'Token not provided.'}, status=HTTP_400_BAD_REQUEST)

#         if not self.is_token_valid(token_key):
#             return Response({'error': 'Invalid token.'}, status=HTTP_400_BAD_REQUEST)

#         # Token is valid, return some data
#         return Response({'message': 'Token is valid.'})


# class CustomTokenLoginView(APIView):  
#     def post(self, request, format=None):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         if user.check_password(password):
#             custom_token = CustomToken.objects.create(user=user)
#             return Response({'token': custom_token.key}, status=status.HTTP_200_OK) 
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class CustomTokenLoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.check_password(password):
                custom_token = CustomToken.objects.create(user=user)
                return Response({'token': custom_token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# token_value = '2c210171bf0d4df879a8b844905fdfa697b32500'
# token = CustomToken.objects.filter(key=token_value).first()
# user_=token.email
# # print(user_)
# User___ = get_user_model()
# user = User___.objects.get(email=user_)
# # print(user.password)
# # email = user.email
# # user_id_parts = user_id.split(',')
# # id = user_id_parts[0]
# # email = user_id_parts[1]
# # print(id)
# # print(email)




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
                uid = urlsafe_base64_encode(force_bytes(user.email))
                token = default_token_generator.make_token(user)

                # Construct the reset URL for the user
                reset_url = request.build_absolute_uri('https://127.0.0.1:8000/user/reset-password/check-query/'+ uid+'/'
                                                       +token+'/')
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
        print("================================== 1 =====================================")
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("================================== 2 =====================================")
        print(request.data)
        uid = request.data.get('user_id')

        print(uid)
        token = request.data.get('token')

        try:
            uid = str(urlsafe_base64_decode(uid), encoding='utf-8', errors='strict')
            print(uid)
            print("================================== 3 =====================================")
            user = User.objects.get(email=uid)
           
            print(user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            print("================================== 4 =====================================")
            user = None
    
        print("================================== 5 =====================================")
        print(default_token_generator.check_token(user,token))
        if user is not None and default_token_generator.check_token(user, token):
            print("================================== 6 =====================================")
            return Response({'uid': uid})
        else:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            msg = _("Unable to find the user's acount with the provided data")
            raise serializers.ValidationError(msg)
        

            

        

class CustomPasswordResetConfirmView(APIView):
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['user_id'])
        
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg)
    
        User.objects.filter(email=serializer.validated_data['user_id']).update(password=make_password(serializer.validated_data['password']))
        
        return Response({'detail': 'Password reset successfully.'})


class EmailVerificationQueryView(APIView):
    serializer_class = EmailVerificationQuerySerializer
    def post(self, request, *args, **kwargs):
        print("================================== 1 =====================================")
        serializer = PasswordResetQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("================================== 2 =====================================")
        print(request.data)
        uid = request.data.get('user_id')

        print(uid)
        token = request.data.get('token')

        try:
            uid = str(urlsafe_base64_decode(uid), encoding='utf-8', errors='strict')
            print(uid)
            print("================================== 3 =====================================")
            user = User.objects.get(email=uid)
           
            # print(user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            print("================================== 4 =====================================")
            user = None
    
        print("================================== 5 =====================================")
        print(default_token_generator.check_token(user,token))
        if user is not None and default_token_generator.check_token(user, token):
            print("================================== 6 =====================================")
            user.is_active=False
            print(user.is_active)
            return Response({'uid': uid})
        else:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            msg = _("Unable to activate the user's acount with the provided data")
            raise serializers.ValidationError(msg)