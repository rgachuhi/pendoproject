
from rest_framework import routers

from .views import UserViewSet

#router = routers.SimpleRouter(trailing_slash=False)
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)


urlpatterns = router.urls
