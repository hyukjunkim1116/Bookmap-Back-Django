from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from .models import User
from django.shortcuts import get_object_or_404


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
        )

    def create(self, validated_data):

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_active(self, user):
        request = self.context["request"]
        return request.user.id == user.id


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        data = super().validate(attrs)

        user = get_object_or_404(User, email=attrs["email"])
        data["email"] = user.email
        data["username"] = user.username
        data["image"] = user.image
        data["social"] = user.is_social_login
        data["is_verified"] = user.is_verified
        return data
