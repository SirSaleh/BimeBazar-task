from rest_framework import serializers

from bookmarks.models import Bookmark
from reviews.models import BookReview


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['book'] 

    def validate(self, data):
        user = self.context['request'].user
        book = data.get('book')
        if Bookmark.objects.filter(user=user, book=book):
            raise serializers.ValidationError("You cannot bookmark a book that you \
                                              have already Bookmarked.")
        if BookReview.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("You cannot bookmark a book that you have \
                                              already reviewed.")
        return data

    def create(self, validated_data):
        return Bookmark.objects.create(**validated_data)