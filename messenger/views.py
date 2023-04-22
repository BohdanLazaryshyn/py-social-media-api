from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Profile, Post
from .serializers import ProfileListSerializer, PostSerializer, ProfileDetailSerializer, OwnerSerializer


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

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.kwargs["username"])
        self.check_object_permissions(self.request, obj)
        return obj


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
            profile = Profile.objects.create(
                user=self.request.user,
                username=self.request.user.username,
                email=self.request.user.email
            )
            return [profile]


class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_queryset(self):
        return self.queryset.exclude(user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPaginationWithSize
