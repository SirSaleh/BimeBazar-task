from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'genre')
    list_filter = ('author', 'genre')


admin.site.register(Book, BookAdmin)
