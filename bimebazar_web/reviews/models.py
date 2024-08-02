from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

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

    def __str__(self):
        return f"Review by {self.user} on {self.book}"