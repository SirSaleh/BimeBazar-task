from django.contrib.auth import get_user_model
from django.urls import reverse
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

