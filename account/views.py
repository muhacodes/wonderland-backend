from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.utils.timezone import now
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import string
import random
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView


class CreateUserView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Assuming you have access and refresh token lifetimes set in your settings
            access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
            refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
            
            response.data["access_token_expires"] = int((now() + access_token_lifetime).timestamp())
            # response.data["refresh_token_expires"] = int((now() + refresh_token_lifetime).timestamp())
        return response



class ChangePasswordView(APIView):
    http_method_names = ['put']

    def put(self, request, format=None):
        serializer =  ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            return Response({'message': 'Successfully Added User to Department'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChangePasswordView(UpdateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ChangePasswordSerializer

#     def update(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InviteUser(APIView):
    def generate_random_password(self, length=8):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
        

    def post(self, request, format=None):
        

        email = request.data.get('email')
        username = request.data.get('username')

        # Generate a random password
        password = self.generate_random_password()


        # Create user account
        user = User.objects.create_user(username=username, email=email, password=password)

        # Prepare context for the email template
        ctx = {
            'username': username,
            'password': password,
            'link' : 'http://localhost:8000/auth/login',
        }

        message = get_template('welcome-user.html').render(ctx)
        msg = EmailMessage(
            'Welcome to your account',
            message,
            'app@lqcollectionstore.com',
            [email],
        )
        msg.content_subtype ="html"# Main content is now text/html
        msg.send()
        return Response({'message': 'Succesfully invited User'}, status=status.HTTP_200_OK)