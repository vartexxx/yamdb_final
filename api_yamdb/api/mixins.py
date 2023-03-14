from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class CategoryMixinViewSet(
    ListCreateAPIView,
    DestroyAPIView,
    GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
