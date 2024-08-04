from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from books.models import Book
from reviews.models import BookReview
from bookmarks.models import Bookmark

User = get_user_model()


class BookReviewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book = Book.objects.create(
            title='Sali Book',
            description='A Sali Book description.',
            author='Sali',
            genre='Sample Genre',
            published_date='2024-08-04'
        )
        self.client.login(username='testuser', password='password')
        self.url = reverse('api:book-reviews-list', kwargs={'book_pk': self.book.pk})

    def test_create_review_success(self):
        data = {
            'rating': 4,
            'review_text': 'This is a great book!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(BookReview.objects.get().rating, 4)
        self.assertEqual(BookReview.objects.get().review_text, 'This is a great book!')

    def test_create_review_with_invalid_rating(self):
        data = {
            'rating': 10,
            'review_text': 'This rating should fail.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'][0], "Rating must be between 1 and 5.")

    def test_create_review_without_rating(self):
        data = {
            'review_text': 'This is a review without a rating.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(BookReview.objects.get().review_text, 'This is a review without a rating.')
        self.assertIsNone(BookReview.objects.get().rating)

    def test_create_review_for_non_existent_book(self):
        invalid_url = reverse('api:book-reviews-list', kwargs={'book_pk': 9999})
        data = {
            'rating': 4,
            'review_text': 'Review for a non-existent book.'
        }
        response = self.client.post(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Book not found.')

    def test_update_existing_review(self):
        BookReview.objects.create(user=self.user, book=self.book, rating=3, review_text='Initial review.')
        data = {
            'rating': 5,
            'review_text': 'Updated review text.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = BookReview.objects.get()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review_text, 'Updated review text.')

    def test_delete_bookmark_when_reviewed(self):
        # Assuming there is a Bookmark model that needs to be checked
        Bookmark.objects.create(user=self.user, book=self.book)
        data = {
            'rating': 3,
            'review_text': 'Bookmarked review.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Bookmark.objects.filter(book=self.book, user=self.user).exists())

