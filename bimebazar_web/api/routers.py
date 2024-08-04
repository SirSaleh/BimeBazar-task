from rest_framework_nested import routers
from .views.book_views import BookViewSet
from .views.bookmark_views import BookmarkViewSet
from .views.book_review_views import BookReviewViewSet

router = routers.DefaultRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

book_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
book_router.register(r'reviews', BookReviewViewSet, basename='book-reviews')