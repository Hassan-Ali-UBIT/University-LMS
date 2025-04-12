# views.py
import random
from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from common.user_exception import CustomAPIException

from .models import User, OTP
from .services import EmailService, OTPService, UserService
from .serializers import (
    RegisterSerializer, LoginSerializer, OTPSerializer, VerifyOTPSerializer,
    ChangePasswordSerializer, UserSerializer, ForgetPasswordSerializer,
    ResetPasswordSerializer, CustomTokenObtainPairSerializer
)

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({"message": "Login successful", "user_id": user.id})

class GenerateOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_type = "forget_password"

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CustomAPIException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        otp_code, otp_minutes = OTPService.create_otp(user, otp_type)
        EmailService.send_otp_email(user.email, otp_code, otp_minutes)

        return Response({"message": "OTP sent successfully"})

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if not serializer.is_valid():
            raise CustomAPIException("Invalid data was given", data=serializer.errors)

        user, otp_type = serializer.validated_data

        if otp_type == "forget_password":
            token = UserService.generate_password_reset_token(user)
            return Response({"message": "OTP verified", "reset_token": token})
        elif otp_type == "sign_up":
            user.is_active = True
            user.save()
            return Response({"message": "OTP verified and account activated"})

class ForgetPasswordResetTokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CustomAPIException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        reset_token = UserService.generate_password_reset_token(user)
        EmailService.send_forget_password_mail_with_token(user.email, reset_token)

        return Response({"message": "Email sent successfully"})

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            raise CustomAPIException("Invalid data was given", data=serializer.errors)
        
        serializer.save()
        return Response({"message": "Password reset successfully"})

class GetUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomAPIException("Invalid data was given", data=serializer.errors)
        serializer.save()
        return Response({"message": "Password changed successfully"})
    

    
