from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from .views import PostViewSet, UserCreateAPIView, AnalyticsListAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = router.urls

urlpatterns += [
    url(r'^users/register/', UserCreateAPIView.as_view(), name='users-create'),
    url(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^analytics/', AnalyticsListAPIView.as_view(), name='analytics')
]
