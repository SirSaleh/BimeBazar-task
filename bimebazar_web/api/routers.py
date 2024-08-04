from rest_framework_nested import routers
from .views.book_views import BookViewSet
from .views.bookmark_views import BookmarkViewSet

router = routers.DefaultRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')