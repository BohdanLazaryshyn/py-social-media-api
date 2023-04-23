from django.urls import path, include
from rest_framework import routers

from messenger.views import (
    PostViewSet,
    OwnerPageView,
    ProfileListView,
    ProfileDetailView, ProfileFollowView,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

app_name = "messenger"

urlpatterns = [
    path("profiles/", ProfileListView.as_view(), name="profiles_list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("", include(router.urls)),
    path("<str:username>/", OwnerPageView.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        }), name="owner-page"),
    path(
        "profiles/<int:pk>/follow/",
        ProfileFollowView.as_view(),
        name="profile_follow",
    ),
]
