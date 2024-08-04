from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.auth_serializers import RegisterUserSerializer


class UserAPIView(APIView):
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='The username of the user',
                                           default="Sali"),
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='The email address of the user',
                                        default="sali@sitesh.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='The password of the user',
                                           default="12345678"),
                'password2': openapi.Schema(type=openapi.TYPE_STRING,
                                            description='Confirm password',
                                            default="12345678")
            },
            required=['username', 'email', 'password', 'password2']
        ),
        responses={
            201: openapi.Response('User registered successfully',
                                  RegisterUserSerializer),
            400: openapi.Response('Bad request',
                                openapi.Schema(type=openapi.TYPE_OBJECT,
                                properties={
                                'error': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='Bad Reqest'),}
                                    )),
            409: openapi.Response('Conflict',
                                openapi.Schema(type=openapi.TYPE_OBJECT,
                                properties={
                                'error': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='Conflict'),}
                                    )),

        }
    )
    def post(self, request, format=None):
        """Create new user (register user)
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            current_users = User.objects.filter(username=
                                                serializer.validated_data['username'])
            if current_users:
                return Response({"error": "user with this username already exists"},
                               status=status.HTTP_409_CONFLICT)
            user = User.objects.create(username=serializer.validated_data['username'],
                                       email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User registered successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
