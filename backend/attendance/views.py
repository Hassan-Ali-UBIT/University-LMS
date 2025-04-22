from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

class StudentAttendanceAPIView(APIView):
    """
    API view to handle student attendance.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve attendance records for a specific student in a course.
        """
        student_id = kwargs.get("student_id")

        # Fetch the attendance records for the given course and student
        attendance_records = AttendanceRecord.objects.filter(student=student_id)

        # Serialize the attendance records
        serializer = AttendanceRecordSerializer(attendance_records, many=True)

        return Response({"attendance_records": serializer.data}, status=status.HTTP_200_OK)
