from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

from reviews.models import BookReview
from ..serializers.book_review_serializers import BookReviewSerializer
from bookmarks.models import Bookmark
from books.models import Book

class BookReviewViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Ensure that 'book_id' is correctly retrieved from kwargs
        book_id = self.kwargs.get('book_pk')
        book = Book.objects.filter(id=book_id).first()
        context['book'] = book
        return context

    @swagger_auto_schema(
        operation_description="Create a new book review",
        request_body=BookReviewSerializer,
        responses={
            201: openapi.Response('Review created successfully', BookReviewSerializer),
            400: 'Invalid input data'
        }
    )
    def create(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_pk')
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        
        Bookmark.objects.filter(book_id=book_id, user=request.user).delete()
        
        return super().create(request, *args, **kwargs)
