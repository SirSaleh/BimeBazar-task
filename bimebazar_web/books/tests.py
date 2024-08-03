from django.test import TestCase
from django.utils import timezone
from .models import Book

class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Sali Book",
            description="This is a test book description.",
            author="Sali",
            genre="Dramatic",
            published_date=timezone.now().date()
        )

    def test_book_creation(self):
        """Test that a Book instance is created correctly."""
        self.assertEqual(self.book.title, "Sali Book")
        self.assertEqual(self.book.description, "This is a test book description.")
        self.assertEqual(self.book.author, "Sali")
        self.assertEqual(self.book.genre, "Dramatic")
        self.assertIsNotNone(self.book.published_date)

    def test_book_str(self):
        """Test the string representation of the Book model."""
        expected_str = f"{self.book.title} by {self.book.author} ({self.book.published_date.year})"
        self.assertEqual(str(self.book), expected_str)
