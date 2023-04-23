from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, generics, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Profile, Post
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedReadOnly
from .serializers import (
    ProfileListSerializer,
    PostSerializer,
    ProfileDetailSerializer,
    OwnerSerializer,
    PostListSerializer,
    PostDetailSerializer,
    FollowerSerializer,
)


class PageNumberPaginationWithSize(PageNumberPagination):
    page_size = 15
    max_page_size = 100


class OwnerPageView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Profile.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if queryset.exists():
            queryset = Profile.objects.all()
            return queryset
        else:
            queryset = Profile.objects.all()
            profile = Profile.objects.create(
                user=self.request.user,
                username=self.request.user.username,
                email=self.request.user.email
            )
            profile.save()
            queryset = queryset.exclude(user=self.request.user)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.kwargs["username"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        user = get_object_or_404(get_user_model(), id=self.request.user.id)
        user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    pagination_class = PageNumberPaginationWithSize
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
        "name",
        "last_name",
        "birth_date",
        "user__email",
    ]

    def get_queryset(self):
        queryset = self.queryset.all()
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(user=self.request.user)
        if self.action == "followers":
            queryset = self.queryset.filter(following=self.request.user.profile)
        if self.action == "following":
            queryset = self.queryset.filter(followers=self.request.user.profile)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return self.serializer_class

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.kwargs["username"])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=False, methods=["get"], url_path="my_posts")
    def followers(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="followers_posts")
    def following(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# class ProfileListView(generics.ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileListSerializer
#     permission_classes = [IsAuthenticatedReadOnly]
#     pagination_class = PageNumberPaginationWithSize
#     filter_backends = [filters.SearchFilter]
#     search_fields = [
#         "username",
#         "name",
#         "last_name",
#         "birth_date",
#         "user__email",
#     ]
#
#     def get_queryset(self):
#         queryset = Profile.objects.all()
#         if self.request.user.is_authenticated:
#             queryset = queryset.exclude(user=self.request.user)
#         return queryset
#
#
# class ProfileDetailView(generics.RetrieveAPIView):
#     queryset = Profile.objects.all()
#     permission_classes = [IsAuthenticatedReadOnly]
#     serializer_class = ProfileDetailSerializer
#
#     def get_queryset(self):
#         return self.queryset.exclude(user=self.request.user)


class ProfileFollowView(generics.GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        following_user = Profile.objects.get(id=pk)
        current_user = self.request.user.profile
        if following_user == current_user:
            return Response(
                {"detail": "forbidden to follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(following_user, data=request.data)

        if serializer.is_valid():

            following_user.toggle_follow(current_user)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPaginationWithSize
    filter_backends = [filters.SearchFilter]
    search_fields = ["text", "author__username", "tags__tag"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    def get_queryset(self):
        queryset = Post.objects.select_related("author").prefetch_related("tags")
        if self.action == "my_posts":
            queryset = queryset.filter(author=self.request.user.profile)
        if self.action == "followers_posts":
            queryset = queryset.filter(author__in=self.request.user.profile.following.all())

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer

        return self.serializer_class

    @action(detail=False, methods=["get"], url_path="my_posts")
    def my_posts(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="followers_posts")
    def followers_posts(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by hashtag id (ex. ?hashtags=2,5)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
