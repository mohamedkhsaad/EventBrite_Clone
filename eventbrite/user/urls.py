from rest_framework import routers
from .views import*
from django.urls import path,include

# router=routers.SimpleRouter()
# router.register('',userViewSet)
# router.register('Interests',user_interests_ViewSet)
# urlpatterns =router.urls

urlpatterns = [
    path('signup/', create_User, name='signup'),
    path('login/',CreateTokenView.as_view(), name='token')
    

]
