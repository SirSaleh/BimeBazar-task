from rest_framework.permissions import BasePermission
from books.models import Book


class BookPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            # everyone can see details of the books
            return True
        else:
            # Only superusers can Create, 
            # Update and delete the Products
            if request.user.is_superuser:
                return True
            return False