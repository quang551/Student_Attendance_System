from student_attendance.cli.auth_cli import login_cli
from student_attendance.cli.menu import show_menu
from student_attendance.repositories.Course_repo import CourseRepo
from student_attendance.repositories.class_repo import ClassRepo
from student_attendance.repositories.db import init_db
from student_attendance.repositories.session_repo import SessionRepo
from student_attendance.repositories.user_repo import UserRepo
from student_attendance.services.Session_service import SessionService
from student_attendance.services.attendance_service import AttendanceService
from student_attendance.services.class_service import ClassService
from student_attendance.services.course_service import CourseService
from student_attendance.services.report_service import ReportService
from student_attendance.services.user_service import UserService


def main():
    print("=== STUDENT ATTENDANCE SYSTEM ===")
    init_db()

    user_repo = UserRepo()
    course_repo = CourseRepo()
    class_repo = ClassRepo()
    session_repo = SessionRepo()

    services = {
        "user_service": UserService(user_repo),
        "course_service": CourseService(course_repo),
        "class_service": ClassService(class_repo, course_repo, user_repo),
        "session_service": SessionService(session_repo, class_repo),
        "attendance_service": AttendanceService(),
        "report_service": ReportService(),
    }

    while True:
        user = login_cli()
        if not user:
            print("Login failed!\n")
            continue

        show_menu(user, services)


if __name__ == "__main__":
    main()
