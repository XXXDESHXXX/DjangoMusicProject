from django.urls import path
from .views import UserFollowCreateAPIView, UserFollowDeleteAPIView

app_name = "users"

urlpatterns = [
    path(
        "follows/create/",
        UserFollowCreateAPIView.as_view(),
        name="user_follow_create",
    ),
    path(
        "follows/delete/<int:user_follow_id>/",
        UserFollowDeleteAPIView.as_view(),
        name="user_follow_delete",
    ),
]
