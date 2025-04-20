# LMS with Attendance Management System - Architecture Document

This is an Architecture Document for Learning Management System (LMS) with integrated Attendance Management System.

**Tech stack:** Next.js + TypeScript + ShadCN UI + Tailwind CSS + Django + Postgres.

## Attendance System:

- The attendance is lesson based and tracked through video watch time
- For each lesson video, system tracks:
  - Total video duration
  - Student's actual watch time
  - Segments watched (to prevent skipping)
  - Watch sessions with timestamps
- Attendance is marked as present if:
  - Student watches >70% of total video duration
  - Student doesn't skip major portions (tracked through segments)

## Role-Based Access Control:

- User can select role of a student or teacher while joining using sign up form.

**TEACHER ROLE:** If a user joins as a Teacher. They can either create only one institution or join multiple institutions as a teacher through a unique institution code.

- If they create an institution, they are the admin of the institution.
  - They can manage students and teachers in the institution.
  - They can CRUD courses inside the institution.
  - They can CRUD lessons inside the courses.
  - They can CRUD comments inside the lessons.
  - They can CRUD replies inside the comments.
  - They can view attendance reports for all students
  - They can approve/reject join requests for the institution

- If they join multiple institutions as a teacher through a unique institution code (TEACHER).
  - They can view all the students and teachers in the institution.
  - They can CRUD their own courses inside the institution.
  - They can CRUD their own lessons inside the courses.
  - They can CRUD their own comments inside the lessons.
  - They can CRUD their own replies inside the comments.
  - They can view all the comments and replies in the institution.
  - They can view attendance for their courses

**STUDENT ROLE:** If a user joins as a student (STUDENT).
  - They can join multiple institutions as a student through a unique institution code.
  - They can view the courses they are assigned to inside the institution.
  - They can view all lessons in the courses.
  - They can view all comments and replies in the lessons.
  - They can CRUD their own comments and replies inside the lessons.
  - They can view their own attendance records
  - They can track their watch progress

**Note:** All the intitutions can generate unique institution code to share with the students and teachers so that they can join the institution. This code can be regenerated and the old code will stop working. This architecture is inspired by Google Classroom.

## Front-end Pages:

1. Landing Page:
  - Hero section with value proposition
  - Key features overview
  - How it works section
  - Testimonials section
  - Call-to-action buttons for sign up
  - Footer with links

2. Authentication Pages:
  - Sign up page with role selection (student/teacher)
  - Sign in page
  - Forgot password page
  - Reset password page

3. Dashboard Pages:
  - Institution dashboard (list of joined institutions)
  - Course dashboard (list of courses with attendance stats)
  - Lesson dashboard (list of lessons with watch progress)
  - Student/Teacher management page (for admin)
  - Profile settings page with account deletion option
  - Attendance analytics and reports page
  - Join requests management page (for admin)

4. Institution Pages:
  - Create institution page
  - Join institution through code modal
  - Institution settings page
  - Institution code management page
  - Institution-wide attendance reports
  - Join request list page

5. Course Pages:
  - Create/Edit course page
  - Course details page with attendance overview
  - Course enrollment page
  - Course attendance requirements settings

6. Lesson Pages:
  - Create/Edit lesson page
  - Lesson view page with:
    - Video player with progress tracking
    - Watch time indicators
    - Comments section
  - Lesson materials upload page
  - Lesson attendance details

UI Requirements:

- Responsive design for mobile and desktop
- Dark/light theme support
- Loading states and error boundaries
- Toast notifications for actions using `sonner`
- Modal confirmations for destructive actions
- Rich text editor for lessons
- File upload interface
- Video player with progress tracking
- Comment threading interface
- Search and filter components
- Pagination for lists
- Form validation feedback
- Attendance visualization components (charts and graphs)
- Account deletion confirmation modal

## Backend API Requirements:

1. Authentication Endpoints:
  - POST /api/auth/register
  - POST /api/auth/login
  - POST /api/auth/forgot-password
  - POST /api/auth/reset-password
  - GET /api/auth/me
  - DELETE /api/auth/me

2. Institution Endpoints:
  - POST /api/institutions
  - GET /api/institutions
  - GET /api/institutions/{id}
  - PUT /api/institutions/{id}
  - DELETE /api/institutions/{id}
  - POST /api/institutions/{id}/generate-code
  - POST /api/institutions/join
  - GET /api/institutions/{id}/members
  - POST /api/institutions/{id}/members
  - DELETE /api/institutions/{id}/members/{userId}
  - GET /api/institutions/{id}/attendance
  - POST /api/institutions/{id}/join-requests
  - GET /api/institutions/{id}/join-requests
  - GET /api/institutions/{id}/join-requests/{requestId}
  - PATCH /api/institutions/{id}/join-requests/{requestId}/     [ pass status=approved in body approved ]
  - PATCH /api/institutions/{id}/join-requests/{requestId}/     [ pass status=rejected in body rejected ]

3. Course Endpoints:
  - POST /api/institutions/{id}/courses
  - GET /api/institutions/{id}/courses
  - GET /api/courses/{id}
  - PUT /api/courses/{id}
  - DELETE /api/courses/{id}
  - GET /api/courses/{id}/students
  - POST /api/courses/{id}/students                             [ for enrolling students ]
  - GET /api/courses/{id}/attendance
  - POST /api/courses/{id}/attendance/requirements              [ not needed as minimum attendance is passed in course creation and can be updated]

4. Lesson Endpoints:
  - POST /api/courses/{id}/lessons
  - GET /api/courses/{id}/lessons
  - GET /api/lessons/{id}
  - PUT /api/lessons/{id}
  - DELETE /api/lessons/{id}
  - GET /api/lessons/{id}/materials
  - POST /api/lessons/{id}/materials
  - POST /api/lessons/{id}/watch-session
  - POST /api/lessons/{id}/watch-segments
  - GET /api/lessons/{id}/attendance
  - GET /api/lessons/{id}/watch-analytics

5. Comment Endpoints:
  - POST /api/lessons/{id}/comments
  - GET /api/lessons/{id}/comments
  - PUT /api/lessons/comments/{id}
  - DELETE /api/lessons/comments/{id}
  - POST /api/lessons/comments/{id}/replies
  - GET /api/lessons/comments/{id}/replies

6. Attendance Endpoints:
  - POST /api/attendance/track
  - GET /api/attendance/student/{id}
  - GET /api/attendance/course/{id}                                   [ Already exists in course ]
  - GET /api/attendance/lesson/{id}                                   [ Already exists in lesson ]
  - GET /api/attendance/analytics
  - GET /api/attendance/export

Database Tables:
1. users
  - id (PK)
  - email
  - password_hash
  - role (student/teacher)
  - name
  - created_at
  - updated_at

2. institutions
  - id (PK)
  - name
  - description
  - join_code
  - admin_id (FK to users)
  - created_at
  - updated_at

3. institution_members
  - id (PK)
  - institution_id (FK to institutions)
  - user_id (FK to users)
  - role (student/teacher)
  - joined_at

4. institution_join_requests
  - id (PK)
  - institution_id (FK to institutions)
  - user_id (FK to users)
  - role (student/teacher)
  - status (pending/approved/rejected)
  - message
  - created_at
  - updated_at

5. courses
  - id (PK)
  - institution_id (FK to institutions)
  - teacher_id (FK to users)
  - name
  - description
  - min_attendance_percent
  - created_at
  - updated_at

6. course_enrollments
  - id (PK)
  - course_id (FK to courses)
  - student_id (FK to users)
  - enrolled_at

7. lessons
  - id (PK)
  - course_id (FK to courses)
  - title
  - content
  - video_duration
  - created_at
  - updated_at

8. lesson_materials
  - id (PK)
  - lesson_id (FK to lessons)
  - file_name
  - file_url
  - file_type
  - uploaded_at

9. comments
  - id (PK)
  - lesson_id (FK to lessons)
  - user_id (FK to users)
  - content
  - created_at
  - updated_at

10. replies
  - id (PK)
  - comment_id (FK to comments)
  - user_id (FK to users)
  - content
  - created_at
  - updated_at

11. watch_sessions
  - id (PK)
  - lesson_id (FK to lessons)
  - student_id (FK to users)
  - start_time
  - end_time
  - watched_duration
  - last_position
  - created_at

12. attendance_records
  - id (PK)
  - lesson_id (FK to lessons)
  - student_id (FK to users)
  - watch_percentage
  - is_present
  - created_at
  - updated_at

13. watch_segments
  - id (PK)
  - watch_session_id (FK to watch_sessions)
  - start_position
  - end_position
  - created_at