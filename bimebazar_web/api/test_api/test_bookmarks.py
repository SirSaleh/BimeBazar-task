from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from books.models import Book
from bookmarks.models import Bookmark
from reviews.models import BookReview

class BookmarkTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.book = Book.objects.create(
            title='Sali Book',
            description='A description of the Sali Book',
            author='Sali',
            genre='Test Genre',
            published_date='2024-01-01'
        )

        self.review = BookReview.objects.create(
            user=self.user,
            book=self.book,
            rating=4,
            review_text='Great book!'
        )

        self.bookmark = Bookmark.objects.create(
            user=self.user,
            book=self.book
        )

        self.another_book = Book.objects.create(
            title='Another Test Book',
            description='A description of another test book',
            author='Another Author',
            genre='Another Genre',
            published_date='2024-05-04'
)

        self.list_url = reverse('api:bookmark-list')
        self.create_url = reverse('api:bookmark-list')
        self.delete_url = reverse('api:bookmark-detail', kwargs={'pk': self.bookmark.pk})

    def authenticate(self):
        self.client.login(username='testuser', password='testpass')

    def test_list_bookmarks(self):
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_create_bookmark_success(self):
        self.authenticate() 
        response = self.client.post(
            self.create_url,
            {'book': self.another_book.pk},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_bookmark(self):
        self.authenticate()
        response = self.client.post(self.create_url, {'book': self.book.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_bookmark_with_review(self):
        self.authenticate()
        response = self.client.post(self.create_url, {'book': self.book.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_bookmark(self):
        self.authenticate()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0) 

    def test_delete_nonexistent_bookmark(self):
        self.authenticate()
        response = self.client.delete(reverse('api:bookmark-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
