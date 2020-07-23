from rest_framework.decorators import action
from rest_framework.response import Response

from . import utils
from .serializers import FanSerializer


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        utils.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        utils.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['GET'])
    def fans(self, request, pk=None):
        obj = self.get_object()
        fans = utils.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
