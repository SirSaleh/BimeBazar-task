from rest_framework_nested import routers
from .views.book_views import BookViewSet

router = routers.DefaultRouter()

router.register(r'books', BookViewSet, basename='book')