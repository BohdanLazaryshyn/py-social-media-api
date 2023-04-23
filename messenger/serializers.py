from django.db import transaction
from rest_framework import serializers
from .models import Profile, Post, Tag


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
            "full_name",
            "profile_picture",
            "bio",
            "birth_date",
        ]


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "full_name",
            "profile_picture",
            "bio",
            "birth_date",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)


class PostSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, allow_empty=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "author", "text", "tags", "created_at", "post_picture"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag=tag_data["tag"])
            post.tags.add(tag)
        return post


class PostListSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer(many=False, read_only=True)
    tags = serializers.StringRelatedField(many=True, allow_empty=True)

    class Meta:
        model = Post
        fields = ["id", "author", "text_preview", "tags", "post_picture"]


class PostDetailSerializer(PostListSerializer):
    tags = serializers.StringRelatedField(many=True, allow_empty=True)

    class Meta:
        model = Post
        fields = ["id", "author", "text", "tags", "created_at", "post_picture"]
