from rest_framework import serializers
from .models import Profile, Post, Tag


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "full_name",
            "profile_picture",
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "profile_picture"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    followers = ProfileListSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "full_name",
            "profile_picture",
            "bio",
            "birth_date",
            "followers",
        ]


class OwnerSerializer(serializers.ModelSerializer):
    subscribers = ProfileListSerializer(source="followers", many=True, read_only=True)
    subscribing = ProfileListSerializer(source="following", many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "full_name",
            "profile_picture",
            "bio",
            "birth_date",
            "subscribers",
            "subscribing",
        ]


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "full_name",
            "profile_picture",
        ]
        read_only_fields = ["username", "full_name", "profile_picture"]


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

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        post = super().update(instance, validated_data)

        post.tags.clear()
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
