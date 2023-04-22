from rest_framework import serializers
from .models import Profile, Post


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "profile_picture"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "email"
            "name",
            "last_name",
            "profile_picture",
            "bio",
            "birth_date",
        ]


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "name",
            "last_name",
            "profile_picture",
            "bio",
            "birth_date",
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
