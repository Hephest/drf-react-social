from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from .views import AnalyticsAPIView, PostViewSet, UserCreateAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = router.urls

urlpatterns += [
    url(r'^users/register/', UserCreateAPIView.as_view(), name='users-create'),
    url(r'^token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^analytics/', AnalyticsAPIView.as_view(), name='analytics')
]
