"""
This module contains 2 view classes for the user app.

class:userViewSet: A viewset for creating a new user (Signup).

class:CreateTokenView: A viewset for the authentication and authorization of the user (login).


"""
from .serializers import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import*
from rest_framework.views import APIView
from eventbrite.settings import *
from django.http import JsonResponse, HttpResponse,HttpResponseBadRequest

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
    serializer_class=AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES



class EmailCheckView(ObtainAuthToken):
    """
    View for checking if an email is in the database.
    """
    serializer_class = EmailCheckSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        Email = serializer.validated_data['email']
        exists = User.objects.filter(email=Email).exists()
        return Response({'exists': exists})

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
