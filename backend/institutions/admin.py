from django.contrib import admin
from .models import Institution, InstitutionMember, InstitutionJoinRequest


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "admin", "join_code", "created_at")
    search_fields = ("name", "admin__email", "join_code")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(InstitutionMember)
class InstitutionMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "role", "joined_at")
    search_fields = ("user__email", "institution__name")
    list_filter = ("joined_at", "role")
    readonly_fields = ("joined_at",)
    ordering = ("-joined_at",)


@admin.register(InstitutionJoinRequest)
class InstitutionJoinRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "role", "status", "created_at")
    search_fields = ("user__email", "institution__name")
    list_filter = ("status", "created_at", "role")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
