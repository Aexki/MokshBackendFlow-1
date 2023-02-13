from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
# Create your views here.


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        username = serializer.data.get("username")
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        content = {"user": username, "email": email}
        return Response(data={'message':"Created", "content":content}, status=status.HTTP_201_CREATED)

class LoginUser(APIView):
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            username = user.username
            response = {"message": "Login Successfull Welcome ", "username": username, "token": user.auth_token.key}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    