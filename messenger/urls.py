from django.urls import path, include
from rest_framework import routers

from messenger.views import (
    PostViewSet,
    OwnerPageView,
    ProfileFollowView,
    ProfileViewSet,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("profiles", ProfileViewSet)

app_name = "messenger"

urlpatterns = [
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
