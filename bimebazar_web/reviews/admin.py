from django.contrib import admin
from .models import BookReview


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'review_text')
    list_filter = ('book', )


admin.site.register(BookReview, BookReviewAdmin)