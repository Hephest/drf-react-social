from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import LikedMixin
from .models import Post, Like
from .serializers import PostSerializer, UserSerializer

User = get_user_model()


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsAPIView(APIView):
    def get(self, request):
        data = Like.objects.extra({'date': 'date(created_at)'}).values('date').annotate(total_likes=Count('id'))
        if not data:
            return Response({'status': 'There is no data available for know.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data, status=status.HTTP_200_OK)
