from django.urls import path

from accounts.views import *

urlpatterns = []
accounts_urls = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile_detail'),
    path('accounts/profiles/', UsersListView.as_view(), name='profile_list'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update'),
    path('profile/change_password/', ChangePasswordView.as_view(), name='change_password'),
]

urlpatterns += accounts_urls 
