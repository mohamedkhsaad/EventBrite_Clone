"""
This module contains 2 view classes for the user app.

class:userViewSet: A viewset for creating a new user (Signup).

class:CreateTokenView: A viewset for the authentication and authorization of the user (login).


"""
from .serializers import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import *
from eventbrite.settings import *
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
# Create your views here.

# import sys
# sys.path.append('/path/to/google-auth')
# importgoogle-api-python-client
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow

# @api_view(['POST'])
# def create_user(request):
#     serializer=userSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     else:
#         Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


'''
user model (EMAIL CHECK)
'''
user_ = get_user_model()
class EmailCheckView(View):
    def get(self, request, email):
        try:
            user = user_.objects.get(email=email)
        except user_.DoesNotExist:
            return JsonResponse({'email_exists': False})
        else:
            return JsonResponse({'email_exists': True})


# class ResetPasswordView(FormView):
#     template_name = 'reset_password.html'
#     form_class = ResetPasswordSerializer
#     success_url = reverse_lazy('password-reset-done')

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class ResetPasswordConfirmView(PasswordResetConfirmView):
#     template_name = 'reset_password_confirm.html'
#     success_url = reverse_lazy('password-reset-complete')

# class PasswordResetCompleteView(APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({'detail': 'Your password has been reset.'}, status=status.HTTP_200_OK)

# class PasswordResetDoneView(APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({'detail': 'We have sent an email to reset your password.'}, status=status.HTTP_200_OK)

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = userSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         # Send email to user with reset password link
#         reset_password_serializer = ResetPasswordSerializer(data=request.data)
#         reset_password_serializer.is_valid(raise_exception=True)
#         reset_password_serializer.send_reset_password_email(user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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


# def google_auth(request):
#     flow = Flow.from_client_config(
#         {
#             'web': {
#                 'client_id': GOOGLE_CLIENT_ID,
#                 'client_secret': GOOGLE_CLIENT_SECRET,
#                 'redirect_uris': [GOOGLE_REDIRECT_URI],
#                 'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
#                 'token_uri': 'https://accounts.google.com/o/oauth2/token',
#                 'access_type': 'offline',
#                 'prompt': 'consent',
#             }
#         },
#         scopes=GOOGLE_AUTH_SCOPES,
#     )
#     authorization_url, state = flow.authorization_url(prompt='consent')
#     request.session['google_auth_state'] = state
#     return redirect(authorization_url)

# def google_auth_callback(request):
#     state = request.session.pop('google_auth_state', None)
#     if state is None:
#         return HttpResponseBadRequest('Invalid state parameter')
#     flow = Flow.from_client_config(
#         {
#             'web': {
#                 'client_id': GOOGLE_CLIENT_ID,
#                 'client_secret': GOOGLE_CLIENT_SECRET,
#                 'redirect_uris': [GOOGLE_REDIRECT_URI],
#                 'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
#                 'token_uri': 'https://accounts.google.com/o/oauth2/token',
#                 'access_type': 'offline',
#                 'prompt': 'consent',
#             }
#         },
#         scopes=GOOGLE_AUTH_SCOPES,
#         state=state,
#     )
#     flow.fetch_token(authorization_response=request.get_full_path())
#     credentials = flow.credentials
#     request.session['google_credentials'] = credentials.to_json()
#     return HttpResponse('Successfully authorized')
