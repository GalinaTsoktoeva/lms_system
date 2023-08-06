from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('view/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-view'),
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(), name='user-edit'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),
]