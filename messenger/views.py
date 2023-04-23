from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, filters, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Profile, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import \
    ProfileListSerializer, \
    PostSerializer, \
    ProfileDetailSerializer, \
    OwnerSerializer, \
    PostListSerializer, \
    PostDetailSerializer


class PageNumberPaginationWithSize(PageNumberPagination):
    page_size = 15
    max_page_size = 100


class OwnerPageView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Profile.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]

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


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
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
        queryset = self.queryset.filter(user=self.request.user)
        if queryset.exists():
            queryset = Profile.objects.all()
            if self.request.user.is_authenticated:
                queryset = queryset.exclude(user=self.request.user)
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


class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_queryset(self):
        return self.queryset.exclude(user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related("tags", "author")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PageNumberPaginationWithSize
    filter_backends = [filters.SearchFilter]
    search_fields = ["text", "author__username", "tags__tag"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        # if self.action == "update" or self.action == "partial_update" or self.action == "delete":
        #     return PostSerializer

        return self.serializer_class
#
# class PostListView(generics.ListCreateAPIView):
#     queryset = Post.objects.prefetch_related("tags", "author")
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = PageNumberPaginationWithSize
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["text", "author__username", "tags__tag"]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user.profile)
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.prefetch_related("tags", "author")
#     serializer_class = PostDetailSerializer
#     permission_classes = [IsOwnerOrReadOnly]

