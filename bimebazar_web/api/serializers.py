from rest_framework import serializers
from books.models import Book
from bookmarks.models import Bookmark


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()


class BookDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id']

class BookListSerializer(serializers.ModelSerializer):
    bookmarks_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    # todo: add detail url after implementing it
    # detail_url = serializers.HyperlinkedIdentityField(view_name='book-detail', format='html')

    class Meta:
        model = Book
        fields = ['id', 'title', 'bookmarks_count', 'is_bookmarked']

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(book=obj, user=request.user).exists()
        return False