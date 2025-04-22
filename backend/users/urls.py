# urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,     # refresh
)
from .views import (
    RegisterView, LoginView, GenerateOTPView, VerifyOTPView,
    ChangePasswordView, GetUpdateDeleteUserView,
    ResetPasswordView, CustomTokenObtainPairView,
    ForgetPasswordResetTokenAPIView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('me/', GetUpdateDeleteUserView.as_view(), name='get-update-user'),
    path('forget-password/', ForgetPasswordResetTokenAPIView.as_view(), name="forget-password"),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('django-login/', LoginView.as_view(), name='django-login'),
    path('otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

