from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegisterView, VerifyEmailView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/<str:code>/', VerifyEmailView.as_view(), name='verify_email'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile_edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile_delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),
    # path('update-pass/', updatepassword, name='update_pass'),
]