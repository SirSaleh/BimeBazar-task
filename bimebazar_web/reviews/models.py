from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.db.models import Q

User = get_user_model()

class BookReview(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='book_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Rating") 
    review_text = models.TextField(null=True, blank=True, verbose_name="Review Text") 
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    class Meta:
        verbose_name = "Book Review"
        verbose_name_plural = "Book Reviews"
        unique_together = ('book', 'user')
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name='rating_range'
            ),
        ]

    def __str__(self):
        return f"Review by {self.user} on {self.book}"