from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.password_validation import validate_password


from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',  'is_admin',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        username = validated_data.get('username')

        # if(len(username) < 4):
        #     raise serializers.ValidationError({'username': ["Username must be at least 4 characters long."]})

        # # Use the create_user method to handle hashing of the password
        # if(len(password) < 6):
        #     raise serializers.ValidationError({'password': ["Password must be at least 6 characters long."]})

        # if(len(username) < 4):
        #     raise serializers.ValidationError({'username': ["Username must be at least 4 characters long."]})
        return User.objects.create_user(**validated_data)
    
    def validate_username(self, value):

        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 Characters long.")
        return value
    
    def validate_password(self, value):

        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 Characters long.")
        return value




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = UserSerializer(user).data
        # ...

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user or self.context.get('user')
        data['user'] = UserSerializer(user).data
        
        # Calculate and include the expiration times for both tokens
        refresh = self.get_token(self.user)
        
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        # Here we add the expiration time for the access token
        access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME

        data['access_token_expires'] = (datetime.now() + access_token_lifetime).timestamp()
        data['refresh_token_expires'] = (datetime.now() + refresh_token_lifetime).timestamp()
        
        return data
    

from django.core.exceptions import ValidationError as DjangoValidationError

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password',)

    def validate_password(self, value):
        print(value)
        raise serializers.ValidationError({"password": {'password' : 'something is surely wrong here'}})

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError({"old_password": "Old password is not correct"})
        return value
