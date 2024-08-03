from django.db.models import Count

from books.models import Book
from ..serializers import BookDetailSerializer, BookListSerializer
from ..permissions import BookPermission
from ..paginations import BookPagination

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets


class BookViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [BookPermission, ]
    pagination_class = BookPagination
    serializer_class = BookListSerializer

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        queryset = Book.objects.annotate(
            bookmarks_count=Count('bookmarks')
        ).order_by('-id').prefetch_related('bookmarks')
        return queryset
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer token for authentication, If you not set, \
                    session authentication will work. The true format for the JWR token\
                        is "Bearer <your access token>" (Don\'t forget the Bearer keywork).',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """get the list of books
        """
        return super().list(self, request, *args, **kwargs)
        