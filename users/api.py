from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import RegisterSerializer, LoginSerializer


class RegisterAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email'])
        if user:
            return Response(
                {'message': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            is_active=True
        )
        return Response(
            {'email': user.email}, status=status.HTTP_201_CREATED
        )


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        fixed_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzcyOTAyLCJpYXQiOjE3NDAxNjgxMDIsImp0aSI6ImQyYmI2MGI2YmJkNDQxOTQ5ZDMzMjg2ZjQwM2EyNjFhIiwidXNlcl9pZCI6MX0.HgabOFp4bdgzGf0qnNa4oq48m6EvCm9nY3ZFEFs4l9I'

        return Response(
            {
                'token': fixed_token
            }, status=status.HTTP_200_OK
        )
