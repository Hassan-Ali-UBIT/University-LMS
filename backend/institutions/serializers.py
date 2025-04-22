from rest_framework import serializers

from users.models import User, Role
from users.serializers import (
    UserSerializer, RoleSerializer
)
from users.services import RoleService

from .models import (
    Institution, InstitutionMember,
    InstitutionJoinRequest
)

from .services import (
    InstituitionService
)

class InstitutionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Institution
        fields = ['id', 'name', 'description', 'join_code', 'admin', 'created_at', 'updated_at']
        read_only_fields = ['admin', 'join_code', 'created_at', 'updated_at']

    def create(self, validated_data):
        

        join_code = InstituitionService.generate_unique_code(
            Institution, "join_code", 8
        )

        validated_data['join_code'] = join_code

        institution = super().create(validated_data)
        
        # Automatically add the admin as a member with ADMIN role
        InstitutionMember.objects.create(
            institution=institution,
            user=institution.admin,
            role=RoleService.get_admin_role()
        )
        
        return institution
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['admin'] = UserSerializer(instance.admin).data

        return representation

class InstitutionMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InstitutionMember
        fields = ['id', 'institution', 'user', 'role', 'joined_at']
        extra_kwargs = {
            "joined_at": {"read_only": True},
            "institution": {"write_only": True, "required": False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['user'] = UserSerializer(instance.user).data
        representation['role'] = RoleSerializer(instance.role).data

        return representation

class InstitutionJoinCodeRequestSerializer(serializers.Serializer):
    join_code = serializers.CharField()
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.exclude(
            id=RoleService.get_admin_role().id
        )
    )

class InstitutionJoinRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InstitutionJoinRequest
        fields = "__all__"
        read_only_fields = ['id', 'user', 'institution', 'status', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['user'] = UserSerializer(instance.user).data
        representation['institution'] = InstitutionSerializer(instance.institution).data

        return representation


# class InstitutionMemberSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     user_id = serializers.UUIDField(write_only=True)
#     institution = InstitutionSerializer(read_only=True)
#     institution_id = serializers.UUIDField(write_only=True)
    
#     class Meta:
#         model = InstitutionMember
#         fields = ['id', 'institution', 'institution_id', 'user', 'user_id', 'role', 'joined_at']
#         read_only_fields = ['id', 'joined_at']


# class InstitutionJoinRequestSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     institution = InstitutionSerializer(read_only=True)
#     institution_id = serializers.UUIDField(write_only=True, required=False)
    
#     class Meta:
#         model = InstitutionJoinRequest
#         fields = ['id', 'institution', 'institution_id', 'user', 'role', 'status', 'message', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         user = self.context['request'].user
#         return InstitutionJoinRequest.objects.create(user=user, **validated_data) 