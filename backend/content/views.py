from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.user_exception import CustomAPIException
from common.debug import print_parameters
from common.cloudfare_utils import upload_file_to_r2
# Create your views here.   
from users.permissions import IsTeacher

from courses.permissions import (
    IsCourseOwner,
    IsCourseStudent
)

from institutions.permissions import (
    IsInstitutionAdminOfCourse
)

from attendance.models import (
    AttendanceRecord,
)

from attendance.serializers import (
    AttendanceRecordSerializer,
)

from .models import (
    Lesson,
    LessonMaterial,
    WatchSegment,
    WatchSession,
)

from .serializers import (
    LessonSerializer,
    LessonMaterialSerializer,
    CommentSerializer,
    ReplySerializer,
    WatchSessionSerializer,
    WatchSegmentSerializer,
)

from .services import (
    WatchSessionService,
    WatchSegmentService,
)

from .permissions import (
    IsInstitutionAdminOfLesson,
)

class LessonAPIView(APIView):
    permission_classes = [(IsCourseOwner | IsInstitutionAdminOfCourse)]

    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        # Serialize the lesson
        serializer = LessonSerializer(lesson_instance)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        self.check_object_permissions(request, lesson_instance.course)

        # Update the lesson
        serializer = LessonSerializer(lesson_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        self.check_object_permissions(request, lesson_instance.course)
        # Delete the lesson
        lesson_instance.delete()
        return Response({"message": "Lesson deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LessonMaterialAPIView(APIView):
    permission_classes = [(IsCourseOwner | IsInstitutionAdminOfCourse)]

    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson material from the database
        lesson_material = LessonMaterial.objects.filter(lesson=lesson_id)

        # Serialize the lesson material
        serializer = LessonMaterialSerializer(lesson_material, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        self.check_object_permissions(request, lesson_instance.course)

        # Create a new lesson material
        lesson_material_serializer = LessonMaterialSerializer(data=request.data)
        lesson_material_serializer.is_valid(raise_exception=True)

        materials = lesson_material_serializer.validated_data.pop("materials", None)

        all_materials = []

        for material in materials:
            file_url = upload_file_to_r2(
                material.name, material, "lesson-materials", lesson_id
            )

            lesson = LessonMaterial(
                lesson=lesson_instance,
                file_name=material.name,
                file_type=material.content_type,
                file_url=file_url,
            )

            all_materials.append(lesson)

        all_material_instance = LessonMaterial.objects.bulk_create(all_materials)

        lesson_material_serializer = LessonMaterialSerializer(
            all_material_instance, many=True
        )

        return Response({"data": lesson_material_serializer.data}, status=status.HTTP_201_CREATED)
    
class WatchSessionAPIView(APIView):
    permission_classes = [(IsCourseStudent | IsCourseOwner | IsInstitutionAdminOfCourse)]

    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the watch session from the database
        watch_session = WatchSession.objects.filter(lesson=lesson_id, student=request.user)

        # Serialize the watch session
        watch_serializer = WatchSessionSerializer(watch_session, many=True)


        return Response({"data": watch_serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        self.check_object_permissions(request, lesson_instance.course)

        # Check if the user is already watching the lesson
        WatchSessionService.validate_watch_session_not_exists(request, lesson_id)

        # Create a new watch session
        watch_session_serializer = WatchSessionSerializer(data=request.data)
        watch_session_serializer.is_valid(raise_exception=True)
        watch_session_serializer.save(
            lesson=lesson_instance,
            student=request.user,
            last_position="0:00:00",
            watched_duration=0,
        )   
        
        return Response({"data": watch_session_serializer.data}, status=status.HTTP_201_CREATED)

class WatchSegmentAPIView(APIView):
    permission_classes = [(IsCourseStudent | IsCourseOwner | IsInstitutionAdminOfCourse)]

    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the watch segment from the database
        watch_session = WatchSession.objects.filter(lesson=lesson_id, student=request.user)

        if not watch_session.exists():
            return Response(
                {"error": "Watch session does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        watch_session_instance = watch_session.first()

        watch_segment = WatchSegment.objects.filter(watch_session=watch_session_instance)

        # Serialize the watch segment
        watch_segment_serializer = WatchSegmentSerializer(watch_segment, many=True)

        return Response({"data": watch_segment_serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        # Fetch the lesson from the database
        lesson_instance = get_object_or_404(Lesson, id=lesson_id)

        self.check_object_permissions(request, lesson_instance.course)

        # Fetch the watch session from the database
        watch_session = WatchSession.objects.filter(lesson=lesson_id, student=request.user)

        if not watch_session.exists():
            return Response(
                {"error": "Watch session does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        watch_session_instance = watch_session.first()

        # Create a new watch segment
        watch_segment_serializer = WatchSegmentSerializer(data=request.data)
        
        watch_segment_serializer.is_valid(raise_exception=True)

        if watch_session_instance.end_time < watch_segment_serializer.validated_data["end_position"]:
            raise CustomAPIException("end position must be less than or equal to end time.")
        
        start_position = watch_segment_serializer.validated_data["start_position"]
        end_position = watch_segment_serializer.validated_data["end_position"]
        
        if WatchSegmentService.validate_no_overlap(start_position, end_position, watch_session_instance):
            
            watch_segment_instance = watch_segment_serializer.save(watch_session=watch_session_instance)

            WatchSegmentService.update_watch_session(watch_segment_instance)

            WatchSessionService.create_attendance_if_necessary(watch_session_instance)
        
            return Response({"data": watch_segment_serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(
            {"message": "segments are overlapping so not counted"},)

class AttendanceRecordAPIView(APIView):
    permission_classes = [IsTeacher | IsInstitutionAdminOfLesson]
    
    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get("lesson_id")

        attendance_record = AttendanceRecord.objects.filter(
            student=request.user,
            lesson=lesson_id
        )

        attendance_record_serializer = AttendanceRecordSerializer(attendance_record, many=True)

        return Response({"data": attendance_record_serializer.data}, status=status.HTTP_200_OK)
