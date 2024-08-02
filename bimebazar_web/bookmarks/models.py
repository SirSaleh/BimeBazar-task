from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Bookmark(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    class Meta:
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
        unique_together = ('book', 'user')

    def __str__(self):
        return f"Bookmark by {self.user} on {self.book}"
