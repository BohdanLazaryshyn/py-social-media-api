from django.urls import path, include
from rest_framework import routers

from messenger.views import PostViewSet, OwnerViewSet, ProfileListView

router = routers.DefaultRouter()
# router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("owner", OwnerViewSet)

app_name = "messenger"

urlpatterns = [
    path("profiles_list/", ProfileListView.as_view(), name="profiles_list"),
    path("", include(router.urls)),
    path("", include(router.urls)),
    path("", include(router.urls)),
]
