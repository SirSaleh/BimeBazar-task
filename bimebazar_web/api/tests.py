from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import Book
from bookmarks.models import Bookmark
from reviews.models import BookReview

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.passwords = {
            'first_user': 'sjdofjoewfosvjvsjdv'
        }
        self.first_user = User.objects.create_user(username="sali",
                                                   password=self.passwords['first_user'])

    def test_get_jwt_token(self):
        # a request without body
        # is a bad request
        response = self.client.post(reverse('api:token_obtain_pair'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # a non-exist user 
        # should return with status-code 401
        response = self.client.post(reverse('api:token_obtain_pair'),
                                    data={'username': '4feefsfsd', 'password': 'fdfdf'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # a wrong credentials for
        # existing user: should return 401
        response = self.client.post(reverse('api:token_obtain_pair'),
                                    data={'username': self.first_user.username,
                                          'password': self.passwords['first_user']+"---"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # a true username password
        # should return the tokens with status 200
        response = self.client.post(reverse('api:token_obtain_pair'),
                                    data={'username': self.first_user.username,
                                          'password': self.passwords['first_user']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user_endpoint(self):
        """tests create use endpoint
        """

        # test conflict in username
        response = self.client.post(reverse("api:users_api_view"), data={
            'username': 'sali',
            'email': 'davsd@sdfdsd.com',
            'password': 'sdfsdf',
            'password2': 'dsdfdsf'
        })

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # test non- complete request boddy in username
        response = self.client.post(reverse("api:users_api_view"), data={
            'username': 'sali2',
            'password': 'sdfsdf',
            'password2': 'dsdfdsf'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test new user creation request boddy in username
        response = self.client.post(reverse("api:users_api_view"), data={
            'username': 'sali2',
            'email': 'davsd@sdfdsd.com',
            'password': 'sdfsdf',
            'password2': 'dsdfdsf'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sali', password='abcdef')
        
        self.token = RefreshToken.for_user(self.user).access_token
        self.books = [
            Book.objects.create(title='Book 1', description='Description 1', author='Author 1', genre='Genre 1'),
            Book.objects.create(title='Book 2', description='Description 2', author='Author 2', genre='Genre 2'),
        ]

        self.bookmark = Bookmark.objects.create(book=self.books[0], user=self.user)

        self.books[0].bookmarks.add(self.bookmark)
        self.url = reverse('api:book-list')

    def test_list_books_authenticated(self):
        """Test listing books when authenticated with JWT token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(self.books))

        for book in response.data['results']:
            if book['id'] == self.books[0].id:
                self.assertTrue(book['is_bookmarked'])
            else:
                self.assertFalse(book['is_bookmarked'])

    def test_list_books_unauthenticated(self):
        """Test listing books when not authenticated."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(self.books))

        for book in response.data['results']:
            self.assertFalse(book['is_bookmarked'])

    def test_list_books_with_pagination(self):
        """Test pagination in the book list."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(self.url + '?page=1&page_size=1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 

    def test_list_books_with_invalid_token(self):
        """Test listing books with an invalid JWT token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books_no_auth(self):
        """Test listing books without providing an authorization header."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDetailAPITestCase(APITestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(username='testuser1', password='testpassword1'),
            User.objects.create_user(username='testuser2', password='testpassword2'),
            User.objects.create_user(username='testuser3', password='testpassword3'),
            User.objects.create_user(username='testuser4', password='testpassword4'),
            User.objects.create_user(username='testuser5', password='testpassword5'),
            User.objects.create_user(username='testuser6', password='testpassword6'),
        ]
        self.book = Book.objects.create(
            title='Test Book',
            description='A book for testing purposes.',
            author='Test Author',
            genre='Fiction',
            published_date='2023-01-01'
        )

        ratings = [5, 2, None, 3, 1, 1]
        reviews = ["khoobe", "not bad", "good", None, None, None]
        for i in range(6):
            BookReview.objects.create(
                book=self.book,
                user=self.users[i],
                rating=ratings[i],
                review_text=reviews[i]
            )

        test_bookmark = Bookmark.objects.create(book=self.book, user=self.users[1])
        self.book.bookmarks.add(test_bookmark)

    def test_book_detail(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(reverse('api:book-detail', kwargs={"pk": self.book.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data['id'], self.book.id)
        self.assertEqual(data['title'], 'Test Book')
        self.assertEqual(data['description'], 'A book for testing purposes.')
        self.assertEqual(data['number_of_reviews'], 3)
        self.assertEqual(data['number_of_ratings'], 5)
        self.assertEqual(data['average_rating'], 2.4)
        self.assertDictEqual(data['ratings_distribution'], {'1': 2, '2': 1, '3': 1, '4': 0, '5': 1})
        
        self.assertEqual(len(data['reviews']), 3)
        for review in data['reviews']:
            self.assertIn('user', review)
            self.assertIn('rating', review)
            self.assertIn('review_text', review)
            self.assertIn('created_at', review)