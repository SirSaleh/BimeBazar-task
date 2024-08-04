from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bookmarks.models import Bookmark
from ..serializers.bookmark_serializers import BookmarkCreateSerializer


class BookmarkViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = BookmarkCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all bookmarks for the authenticated user",
        responses={200: openapi.Response('Successful Response', BookmarkCreateSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """
        List all bookmarks for the authenticated user.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new bookmark",
        request_body=BookmarkCreateSerializer,
        responses={
            201: openapi.Response('Bookmark created successfully', BookmarkCreateSerializer),
            400: 'Invalid input data'
        }
    )

    def get_queryset(self):
        qs = Bookmark.objects.filter(user=self.request.user).order_by('-id')
        return qs

    def create(self, request, *args, **kwargs):
        """
        Create a new bookmark.
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Delete a bookmark",
        responses={
            204: 'Bookmark deleted successfully',
            404: 'Bookmark not found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a bookmark.
        """
        return super().destroy(request, *args, **kwargs)