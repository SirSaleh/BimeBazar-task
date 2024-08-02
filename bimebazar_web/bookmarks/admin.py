from django.contrib import admin
from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book', 'user')


admin.site.register(Bookmark, BookmarkAdmin)