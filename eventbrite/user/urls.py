"""
This module contains 2 url calls for the user app.

userViewSet: a url that calls the class for creating a new user (Signup).

CreateTokenView: a url that calls the class for the authentication and authorization of the user (login).

"""
from rest_framework import routers
from .views import*
from django.contrib.auth import views as auth_views
from django.urls import path,include

router=routers.SimpleRouter()
router.register('',userViewSet)# router.register('Interests',user_interests_ViewSet)
urlpatterns =router.urls

urlpatterns = [
    path('signup/', userViewSet.as_view({'post': 'create'}), name='signup'),
    path('login/', CreateTokenView.as_view(), name='token'),
    path('emailCheck/', EmailCheckView.as_view(), name='email-check'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),

]
