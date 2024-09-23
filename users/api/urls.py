from django.urls import path
from .views import UserFollowCreateAPIView, UserFollowDeleteAPIView, UserFollowListAPIView

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
    path('user/<int:user_id>/follows/', UserFollowListAPIView.as_view(), name='user_follows'),
]
