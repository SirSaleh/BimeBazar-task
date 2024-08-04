from rest_framework import serializers
from reviews.models import BookReview

class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    rating = serializers.IntegerField(
        help_text="Rating for the book. Must be an integer between \
            1 and 5 or use null",
        allow_null=True,
        required=False
    )
    review_text = serializers.CharField(
        help_text="Optional text review of the book.\
              Provide a description of your experience with the book.",
        allow_blank=True, 
        allow_null=True,
        required=False
    )

    class Meta:
        model = BookReview
        fields = ['user', 'rating', 'review_text', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        book = self.context.get('book')
        user = request.user

        if not book:
            raise serializers.ValidationError({"error": "Book must be provided."})

        rating = data.get('rating')
        if rating is not None and not (1 <= rating <= 5):
            raise serializers.ValidationError({"error": "Rating must be between 1 and 5."})

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        book = self.context.get('book')
        return BookReview.objects.update_or_create(
            user=request.user,
            book=book,
            defaults=validated_data
        )[0]
