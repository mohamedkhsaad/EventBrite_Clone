from rest_framework import routers
from .views import eventViewSet

router=routers.SimpleRouter()
router.register('',eventViewSet)
urlpatterns =router.urls
