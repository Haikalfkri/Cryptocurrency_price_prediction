from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError("User not found.")
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("Invalid password.")
        return attrs
    

class CryptoSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoSymbols
        fields = ['name']


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'


class CryptoNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoNews
        fields = [
            'title', 'description', 'summary', 'sentiment', 'image', 'link', 'published_at'
        ]


class CryptoInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoInsight
        fields = ['title', 'link', 'date', 'source', 'image', 'category']