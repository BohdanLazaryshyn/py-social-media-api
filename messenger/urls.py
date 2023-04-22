from django.urls import path, include
from rest_framework import routers

from messenger.views import ProfileViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)

app_name = "messenger"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls)),
]
