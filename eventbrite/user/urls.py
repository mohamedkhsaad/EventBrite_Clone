from rest_framework import routers
from .views import*

router=routers.SimpleRouter()
router.register(r'user',userViewSet)
router.register('Interests',user_interests_ViewSet)
urlpatterns =router.urls
