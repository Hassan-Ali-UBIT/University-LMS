from common.user_exception import CustomAPIException
from common.debug import print_parameters

from rest_framework import status

from .models import (
    Course, CourseEnrollment
)

class CourseService:

    @staticmethod
    def is_member_of_course_institution(course: Course ,user):
        return course.institution.members.filter(user=user).exists()

    @staticmethod
    def validate_member_not_exists_in_course(course: Course, user):
        if CourseEnrollment.objects.filter(course=course, student=user).exists():
            raise CustomAPIException("User is already enrolled in this course.")

    @staticmethod
    def check_student_add_permission(course: Course, user):
        """
        Check if the user has permission to add a student to the course.
        """
        if course.institution.admin != user or course.teacher != user:
            raise CustomAPIException(
                "You do not have permission to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        

