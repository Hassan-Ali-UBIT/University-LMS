import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model that uses email as the primary identifier instead of a username."""
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = ["username"]  # No other required fields except email

    def __str__(self):
        """Return the string representation of the User model."""
        return self.email


class Role(models.Model):
    """Role model that defines different user roles within the system."""
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the Role model."""
        return self.name


class UserProfile(models.Model):
    """UserProfile model that extends the User model with additional fields."""
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile")
    role = models.ForeignKey(Role,
                            on_delete=models.SET_NULL,
                            null=True)
    name = models.CharField(max_length=255,
                            blank=True,
                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the string representation of the UserProfile model."""
        return f"{self.user.email} - {getattr(self.role, 'name', 'No role Defined')}"

class OTP(models.Model):
    otp_type = (
        ("sign_up", "Sign Up"),
        ("forget_password", "Forget Password"),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    type = models.CharField(max_length=100, choices=otp_type)
    used = models.BooleanField(default=False)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} | {self.otp} | {self.expire_at.time().strftime('%H:%M')}"