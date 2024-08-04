from django.db.models import Count, Avg
from django.urls import reverse
from rest_framework import serializers

from books.models import Book
from bookmarks.models import Bookmark
from reviews.models import BookReview

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()

class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = BookReview
        fields = ['user', 'rating', 'review_text', 'created_at']

class BookDetailSerializer(serializers.ModelSerializer):
    number_of_reviews = serializers.SerializerMethodField()
    number_of_ratings = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_distribution = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 
                  'number_of_reviews', 'number_of_ratings', 
                  'average_rating', 'ratings_distribution',
                  'reviews']
    
    def get_number_of_reviews(self, obj):
        return obj.book_reviews.exclude(review_text__isnull=True).count()

    def get_number_of_ratings(self, obj):
        return obj.book_reviews.exclude(rating__isnull=True).count()

    def get_average_rating(self, obj):
        return obj.book_reviews.exclude(rating__isnull=True).aggregate(average_rating=
                                          Avg('rating'))['average_rating']

    def get_ratings_distribution(self, obj):
        distribution = {rating: 0 for rating in range(1, 6)}
        ratings_counts = obj.book_reviews.values('rating').annotate(count=Count('rating'))
        
        for rating_count in ratings_counts:
            rating = rating_count['rating']
            count = rating_count['count']
            if rating in distribution:
                distribution[rating] = count

        return distribution

    def get_reviews(self, obj):
        reviews = obj.book_reviews.exclude(review_text__isnull=True)
        return BookReviewSerializer(reviews, many=True).data

class BookListSerializer(serializers.ModelSerializer):
    bookmarks_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    detail_path = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'bookmarks_count', 'is_bookmarked', 'detail_path']

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(book=obj, user=request.user).exists()
        return False
    
    def get_detail_path(self, obj):
        return reverse('api:book-detail', kwargs={'pk': obj.id})