from cli.auth_cli import login_cli
from cli.menu import show_menu

from services.class_service import ClassService
from services.attendance_service import AttendanceService
from services.report_service import ReportService
from repositories.db import init_db


def main():
    print("=== STUDENT ATTENDANCE SYSTEM ===")
    init_db()

    class_service = ClassService()
    attendance_service = AttendanceService()
    report_service = ReportService()

    while True:
        user = login_cli()

        if user:
            show_menu(
                user,
                class_service,
                attendance_service,
                report_service,
            )
        else:
            print("Login failed!\n")


if __name__ == "__main__":
    main()