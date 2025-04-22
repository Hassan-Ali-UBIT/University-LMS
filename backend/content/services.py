from common.user_exception import CustomAPIException
from common.utils import time_to_seconds

from attendance.models import (
    AttendanceRecord,
)

from .models import (
    WatchSession,
    WatchSegment,
)




class WatchSessionService:

    @staticmethod
    def validate_watch_session_not_exists(request, lesson_id):
        watch_session = WatchSession.objects.filter(lesson=lesson_id, student=request.user)
        if watch_session.exists():
            raise CustomAPIException("Watch session already exists.")
        
    @staticmethod
    def create_attendance_if_necessary(watch_session: WatchSession):

        try:
            total_duration = time_to_seconds(watch_session.end_time)
            if total_duration <= 0:
                raise ValueError("Total duration must be greater than zero.")
        except (TypeError, ValueError) as e:
            # Log error if needed (e.g., logger.error(f"Invalid end_time: {e}"))
            return

        percentage_watched = watch_session.watched_duration / total_duration * 100

        if  percentage_watched >= 75:

            if not watch_session.is_completed:
                watch_session.is_completed = True
                watch_session.save()

            AttendanceRecord.objects.update_or_create(
                student=watch_session.student,
                lesson=watch_session.lesson,
                defaults={
                    "watch_percentage": round(percentage_watched, 2)
                }
            )

class WatchSegmentService:

    @staticmethod
    def validate_start_time(watch_session, start_time):

        last_watch_segment = WatchSegment.objects.filter(
            watch_session=watch_session
        ).order_by('-created_at').first()

        if last_watch_segment and last_watch_segment.end_position > start_time:
            return False
        
        return True
    
    @staticmethod
    def validate_no_overlap(new_start, new_end, session_id):
        overlapping = WatchSegment.objects.filter(
            watch_session_id=session_id,
            start_position__lt=new_end,
            end_position__gt=new_start
        ).exists()
        if overlapping:
            return False
        return True
    
    @staticmethod
    def update_watch_session(watch_segment: WatchSegment):
        watch_session = watch_segment.watch_session
        watch_session.watched_duration += (
            time_to_seconds(watch_segment.end_position) - 
            time_to_seconds(watch_segment.start_position)
        )
        watch_session.last_position = watch_segment.end_position
        watch_session.save()



