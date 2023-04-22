from django.urls import path, include
from rest_framework import routers

from messenger.views import PostViewSet, OwnerPageView, ProfileListView, ProfileDetailView

router = routers.DefaultRouter()
# router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
# router.register("<str:username>", OwnerPageView)

app_name = "messenger"

urlpatterns = [
    path("profiles/", ProfileListView.as_view(), name="profiles_list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profiles/<str:username>/", OwnerPageView.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        }), name="owner_page"),
    path("", include(router.urls)),
    path("", include(router.urls)),
    path("", include(router.urls)),
]
