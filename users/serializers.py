from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from .models import User, Profile, Job, Skill, Product, ChatMessage

# カスタムユーザーを使用しているため、取得するユーザーモデルを指定
User = get_user_model()

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('role', 'username','email','password', 're_password')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['affiliation', 'company', 'industry', 'bio', 'profile_image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "role", "profile"]

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("user",)

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_user = UserSerializer(read_only=True)
    receiver_user = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "user", "sender", "sender_user", "receiver", "receiver_user", "message", "is_read", "created_at"]