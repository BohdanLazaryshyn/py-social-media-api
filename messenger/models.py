import os
import uuid

from django.db import models
from django.utils.text import slugify

from user.models import User


def image_file_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}"
    return os.path.join("uploads/", filename + ext)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=image_file_path, blank=True, null=True
    )
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False
    )

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"

    def toggle_follow(self, profile):
        if profile in self.followers.all():
            profile.followers.remove(self)
        else:
            profile.followers.add(self)

    def __str__(self):
        return self.username


class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag


class Post(models.Model):
    TEXT_PREVIEW_LENGTH = 20

    text = models.TextField(max_length=500)
    tags = models.ManyToManyField(Tag, related_name="tags")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    post_picture = models.ImageField(upload_to=image_file_path, blank=True, null=True)

    @property
    def text_preview(self):
        if len(self.text) <= self.TEXT_PREVIEW_LENGTH:
            return self.text
        return self.text[:self.TEXT_PREVIEW_LENGTH] + "..."

    def __str__(self):
        return self.text
