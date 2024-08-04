from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from books.models import Book
from .models import Bookmark

User = get_user_model()

class BookmarkModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.book = Book.objects.create(
            title="Sali Book",
            description="This is the test book description.",
            author="Sali",
            genre="Fiction",
            published_date=timezone.now().date()
        )

        self.bookmark = Bookmark.objects.create(
            book=self.book,
            user=self.user,
            created_at=timezone.now()
        )

    def test_bookmark_creation(self):
        """Test that a Bookmark instance is created correctly."""
        self.assertEqual(self.bookmark.book, self.book)
        self.assertEqual(self.bookmark.user, self.user)
        self.assertIsNotNone(self.bookmark.created_at)

    def test_unique_together_constraint(self):
        """Test the unique_together constraint on book and user fields."""
        with self.assertRaises(Exception) as raised:
            Bookmark.objects.create(
                book=self.book,
                user=self.user,
                created_at=timezone.now()
            )
        self.assertIn('UNIQUE constraint failed', str(raised.exception))

    def test_bookmark_str(self):
        """Test the string representation of the Bookmark model."""
        expected_str = f"Bookmark by {self.user} on {self.book}"
        self.assertEqual(str(self.bookmark), expected_str)
