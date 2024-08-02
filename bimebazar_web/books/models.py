from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    author = models.CharField(max_length=200, verbose_name="Author")
    genre = models.CharField(max_length=200, verbose_name="Genre")
    published_date = models.DateField(default=timezone.now,
                                    verbose_name="Published Date")


    class Meta:
        verbose_name="Book"
        verbose_name_plural="Books"

    def __str__(self):
        return f"{self.title} by {self.author} ({self.published_date.year})"