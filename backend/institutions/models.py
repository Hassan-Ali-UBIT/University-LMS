import uuid
from django.db import models

from users.models import Role, User


class Institution(models.Model):
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    join_code = models.CharField(max_length=20, unique=True)
    admin = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="managed_institutions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class InstitutionMember(models.Model):
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    related_name="members"
                                    )
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="institution_memberships"
                            )
    # some commnets
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("institution", "user")

class InstitutionJoinRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    related_name="join_requests"
                                    )
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="join_requests"
                            )
    role = models.ForeignKey(Role,
                            on_delete=models.SET_NULL,
                            null=True)
    status = models.CharField(max_length=20,
                            choices=STATUS_CHOICES,
                            default="pending")
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
