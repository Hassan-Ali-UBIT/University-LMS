from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.permissions import IsCourseOwner
from courses.models import Course
from courses.serializers import CourseSerializer

from users.models import User
from users.services import RoleService
from users.permissions import IsTeacher
from users.serializers import UserSerializer

from .models import (
    Institution,
    InstitutionMember, 
    InstitutionJoinRequest
)
from .serializers import (
    InstitutionSerializer, 
    InstitutionMemberSerializer, 
    InstitutionJoinRequestSerializer,
    InstitutionJoinCodeRequestSerializer,
)
from .services import (
    InstituitionService
)
from .permissions import (
    IsInstitutionAdminOrReadOnly,
    IsInstitutionAdmin,
    IsInstitutionMember,
)

# Create your views here.


    


class InstitutionViewSet(viewsets.ModelViewSet):
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher, IsInstitutionAdminOrReadOnly]

    def get_queryset(self):

        institution_ids = InstitutionMember.objects.filter(
            user=self.request.user
        ).values_list('institution', flat=True)

        institutions = Institution.objects.filter(id__in=institution_ids)

        return institutions

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

class InstitutionGenerateCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        institution_id = kwargs.get("institution_id")

        institution_instance = get_object_or_404(Institution,
                                                id=institution_id, 
                                                admin=self.request.user)
        join_code = InstituitionService.generate_unique_code(Institution, "join_code")
        institution_instance.join_code = join_code
        institution_instance.save()

        return Response({"join_code": join_code})

class InstitutionJoinAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        institution_id = kwargs.get("institution_id")
        institution_instance = get_object_or_404(Institution,
                                                id=institution_id)
        
        join_request_serializer = InstitutionJoinCodeRequestSerializer(data=request.data)

        join_request_serializer.is_valid(raise_exception=True)

        join_code = join_request_serializer.validated_data["join_code"]
        join_role = join_request_serializer.validated_data["role"]

        if institution_instance.join_code != join_code:
            return Response({"error": "Invalid code was passed"}, status=status.HTTP_400_BAD_REQUEST)
        
        if InstitutionMember.objects.filter(
            institution=institution_instance, user=request.user
            ).exists():
            return Response(
                {"error": "You are already a member of this institution."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        InstitutionMember.objects.create(
            institution=institution_instance,
            user=request.user,
            role=join_role
        )

        return Response({"message": "request made successfully"}, status=status.HTTP_201_CREATED)

class InstitutionMemberAPIView(APIView):
    permission_classes = [IsInstitutionAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        institution_id = kwargs.get("institution_id")

        institution_members_queryset = InstitutionMember.objects.filter(
            institution=institution_id
        )

        institution_members_serializer = InstitutionMemberSerializer(
                                        institution_members_queryset, many=True
                                    )

        return Response({"data": institution_members_serializer.data})
    
    def post(self, request, *args, **kwargs):
        institution_id = kwargs.get("institution_id")

        institution_instance = get_object_or_404(Institution,
                                                id=institution_id)
        
        institution_member_serializer = InstitutionMemberSerializer(data=request.data)

        institution_member_serializer.is_valid(raise_exception=True)

        institution_member_serializer.save(institution=institution_instance)

        return Response({"message": "member added successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        institution_id = kwargs.get("institution_id")
        user_id = kwargs.get("user_id")

        institution_member = get_object_or_404(InstitutionMember, 
                                            institution=institution_id,
                                            user=user_id)
        
        if request.user == institution_member.user:
            return Response({"error": "you cannot remove yourself"}, status=status.HTTP_400_BAD_REQUEST) 
        
        institution_member.delete()

        return Response({"message": "member removed successfully"}, status=status.HTTP_204_NO_CONTENT)

class InstitutionJoinRequestAPIView(APIView):
    permission_classes = [IsInstitutionAdmin]
    def get(self, request, *args, **kwargs):

        institution_id = kwargs.get("institution_id")
        request_id = kwargs.get("request_id")

        institution_instance = get_object_or_404(Institution, id=institution_id)

        self.check_object_permissions(request, institution_instance)

        if request_id:
            
            join_request = get_object_or_404(InstitutionJoinRequest,
                                            id=request_id,
                                            institution=institution_id)
            
            join_request_serializer = InstitutionJoinRequestSerializer(
                join_request
            )

            return Response({"data": join_request_serializer.data})
        
        join_request_queryset = InstitutionJoinRequest.objects.filter(
                                    institution=institution_id
                                )
        
        join_request_serializer = InstitutionJoinRequestSerializer(
            join_request_queryset, many=True
        )

        return Response({"data": join_request_serializer.data})

    def post(self, request, *args, **kwargs):

        institution_id = kwargs.get("institution_id")

        institution_instance = get_object_or_404(Institution, id=institution_id)

        if InstitutionMember.objects.filter(
            institution=institution_instance, user=request.user
            ).exists():
            return Response(
                {"error": "You are already a member of this institution."},
                status=status.HTTP_400_BAD_REQUEST
            )

        join_request_serializer = InstitutionJoinRequestSerializer(
                data=request.data
            )
        
        join_request_serializer.is_valid(raise_exception=True)

        join_request_serializer.save(institution=institution_instance, user=request.user)

        return Response({"message": "request created successfully"}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        institution_id = kwargs.get("institution_id")
        request_id = kwargs.get("request_id")

        institution_instance = get_object_or_404(Institution, id=institution_id)

        self.check_object_permissions(request, institution_instance)

        request_instance = get_object_or_404(InstitutionJoinRequest,
                                            id=request_id,
                                            institution=institution_id, 
                                            status="pending")
        
        req_status = request.data.get("status")

        if req_status not in ["approved", "rejected"]:
            return Response({"error": "invalid value for status was passed"}, status=status.HTTP_400_BAD_REQUEST)
        
        request_instance.status = req_status
        request_instance.save()

        if req_status == "approved":

            InstitutionMember.objects.create(
                institution=institution_instance,
                user=request_instance.user, 
                role=request_instance.role
            )

            return Response({"message": "Request Approved successfully"})
        
        else:
            return Response({"message": "Request Rejected successfully"})

class InstitutionCoursesAPIView(APIView):
    permission_classes = [(IsTeacher | IsInstitutionAdmin)]
    
    def get(self, request, *args, **kwargs):
        
        institution_id = kwargs.get("institution_id")

        course_queryset = Course.objects.filter(institution=institution_id)

        course_queryset_serializer = CourseSerializer(course_queryset, many=True)

        return Response({"data": course_queryset_serializer.data})
    
    def post(self, request, *args, **kwargs):

        institution_id = kwargs.get("institution_id")

        institution_instance = get_object_or_404(Institution, id=institution_id)

        course_serializer = CourseSerializer(data=request.data)

        course_serializer.is_valid(raise_exception=True)

        course_serializer.save(institution=institution_instance, teacher=request.user)

        return Response({"message": "Course Created Successfully"}, status=status.HTTP_201_CREATED)



