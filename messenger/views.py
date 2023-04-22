from rest_framework import mixins, generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Profile, Post
from .serializers import ProfileListSerializer, PostSerializer, ProfileDetailSerializer, OwnerSerializer


class PageNumberPaginationWithSize(PageNumberPagination):
    page_size = 15
    max_page_size = 100


class OwnerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Profile.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPaginationWithSize
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
        "last_name",
        "birth_date",
        "user__email",
    ]

    def get_queryset(self):
        queryset = Profile.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(user=self.request.user)
        return queryset
#
#
# class ProfileViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileListSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = PageNumberPaginationWithSize
#
#     def get_queryset(self):
#         queryset = Profile.objects.all()
#         username = self.request.query_params.get("username", None)
#         first_name = self.request.query_params.get("first_name", None)
#         last_name = self.request.query_params.get("last_name", None)
#         if username:
#             queryset = queryset.filter(username__icontains=username)
#         if first_name:
#             queryset = queryset.filter(first_name__icontains=first_name)
#         if last_name:
#             queryset = queryset.filter(last_name__icontains=last_name)
#         if self.request.user.is_authenticated:
#             queryset = queryset.exclude(user=self.request.user)
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == "retrieve":
#             return ProfileDetailSerializer
#         return self.serializer_class


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPaginationWithSize
