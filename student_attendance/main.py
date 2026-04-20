from cli.auth_cli import login_cli
from cli.menu import show_menu
from repositories.Course_repo import CourseRepo
from repositories.class_repo import ClassRepo
from repositories.db import init_db
from repositories.session_repo import SessionRepo
from repositories.user_repo import UserRepo
from services.Session_service import SessionService
from services.attendance_service import AttendanceService
from services.class_service import ClassService
from services.course_service import CourseService
from services.report_service import ReportService
from services.user_service import UserService


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
