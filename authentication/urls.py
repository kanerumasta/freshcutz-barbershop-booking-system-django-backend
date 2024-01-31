from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
  
  path('register',RegisterView.as_view()),
  path('token', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
  path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
  path('verify-otp', VerifyOTPView.as_view()),
  path('is-unique-email/<str:email>', is_unique_email),
  path('users', UserListCreateAPIView.as_view(), name="users-list"),
  path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name="users-detail"),
  path('users/suspend', suspend_user, name="suspend-user"),
]