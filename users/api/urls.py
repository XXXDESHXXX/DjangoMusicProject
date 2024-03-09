from django.urls import path
from .views import UserFollowCreateAPIView, UserFollowDeleteAPIView

app_name = 'users'

urlpatterns = [
    path('users/follows/create/', UserFollowCreateAPIView.as_view(), name='user_follow_create'),
    path("users/follows/delete/<int:user_id>/", UserFollowDeleteAPIView.as_view(), name='user_follow_delete'),
]
