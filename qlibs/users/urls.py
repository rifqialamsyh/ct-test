from django.urls import path
from .views import Register, Login, UserListView, UserDetailView

urlpatterns = [
    path('register/', Register.as_view(), name='register_user'),
    path('login/', Login.as_view(), name='login_user'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
]
