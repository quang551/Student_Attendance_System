def _print_result(success, message):
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def _print_sessions(session_service):
    if not session_service:
        return

    sessions = session_service.list_sessions()
    print("\n===== SESSION LIST =====")
    if not sessions:
        print("No sessions found.")
        return

    print("Session ID | Class ID | Start Time | End Time | Status")
    for session in sessions:
        status = "OPEN" if session.is_open else "CLOSED"
        print(
            f"{session.session_id} | "
            f"{session.class_id} | "
            f"{session.start_time or '-'} | "
            f"{session.end_time or '-'} | "
            f"{status}"
        )


def _print_students_of_session(attendance_service, class_service, session_id):
    class_id = attendance_service.get_class_id_by_session(session_id)
    if not class_id:
        print("❌ Class not found for this session.")
        return False

    ok, message, students = class_service.list_students(class_id)
    if not ok:
        print(f"❌ {message}")
        return False

    print(f"\n===== STUDENTS IN CLASS {class_id} =====")
    if not students:
        print("No students found in this class.")
        return True

    print("Student ID | Full Name | Username | Email")
    for student in students:
        print(
            f"{student['student_id']} | "
            f"{student['full_name']} | "
            f"{student['user_name']} | "
            f"{student['email']}"
        )
    return True


def _manage_attendance_session(attendance_service, session_service):
    if not session_service:
        print("❌ Session management is not available in this menu.")
        return

    while True:
        _print_sessions(session_service)

        print("\n===== ATTENDANCE SESSION MANAGEMENT =====")
        print("1. Create session")
        print("2. Open session")
        print("3. Close session")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            session_id = input("Session ID: ").strip()
            class_id = input("Class ID: ").strip()
            result = session_service.create_session(session_id, class_id)
            _print_result(result[0], result[1])

        elif choice == "2":
            session_id = input("Session ID: ").strip()
            _print_result(*attendance_service.open_session(session_id))

        elif choice == "3":
            session_id = input("Session ID: ").strip()
            _print_result(*attendance_service.close_session(session_id))

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def _take_attendance(attendance_service, session_service, class_service):
    _print_sessions(session_service)

    session_id = input("Session ID: ").strip()

    if not attendance_service.is_session_open(session_id):
        print("❌ Session is not open or does not exist.")
        return

    if class_service:
        _print_students_of_session(attendance_service, class_service, session_id)

    while True:
        print("\n1. Take attendance")
        print("0. Back")
        sub_choice = input("Choose: ").strip()

        if sub_choice == "1":
            attendance_id = input("Attendance ID: ").strip()
            student_id = input("Student ID: ").strip()
            print("1. Present | 2. Absent | 3. Late")
            status = input("Status: ").strip()

            if not status.isdigit():
                print("❌ Invalid status.")
                continue

            _print_result(
                *attendance_service.mark_attendance(
                    attendance_id,
                    session_id,
                    student_id,
                    int(status),
                )
            )

        elif sub_choice == "0":
            break

        else:
            print("Invalid choice.")


def _edit_attendance(attendance_service, session_service, class_service):
    _print_sessions(session_service)

    session_id = input("Session ID: ").strip()

    if class_service:
        _print_students_of_session(attendance_service, class_service, session_id)

    print("\n===== CURRENT ATTENDANCE RECORDS =====")
    data = attendance_service.view_attendance_by_session(session_id)
    if not data:
        print("No attendance records found for this session.")
    else:
        for row in data:
            print(row)

    while True:
        print("\n1. Edit / add attendance")
        print("0. Back")
        sub_choice = input("Choose: ").strip()

        if sub_choice == "1":
            attendance_id = input("Attendance ID: ").strip()
            student_id = input("Student ID: ").strip()
            print("1. Present | 2. Absent | 3. Late")
            status = input("New status: ").strip()

            if not status.isdigit():
                print("❌ Invalid status.")
                continue

            _print_result(
                *attendance_service.mark_attendance(
                    attendance_id,
                    session_id,
                    student_id,
                    int(status),
                )
            )

        elif sub_choice == "0":
            break

        else:
            print("Invalid choice.")


def attendance_menu(attendance_service, session_service=None, class_service=None, user=None, role=None):
    if role == "student":
        _student_attendance_menu(attendance_service, user)
        return

    while True:
        _print_sessions(session_service)

        print("\n===== ATTENDANCE MENU =====")
        print("1. Manage attendance sessions")
        print("2. Take attendance")
        print("3. Edit attendance")
        print("4. View attendance by session")
        print("5. View attendance by student")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            _manage_attendance_session(attendance_service, session_service)

        elif choice == "2":
            _take_attendance(attendance_service, session_service, class_service)

        elif choice == "3":
            _edit_attendance(attendance_service, session_service, class_service)

        elif choice == "4":
            _print_sessions(session_service)
            session_id = input("Session ID: ").strip()
            data = attendance_service.view_attendance_by_session(session_id)
            if not data:
                print("No attendance data found.")
            for row in data:
                print(row)

        elif choice == "5":
            student_id = input("Student ID: ").strip()
            data = attendance_service.view_attendance_by_student(student_id)
            if not data:
                print("No attendance data found.")
            for attendance in data:
                print(attendance)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def _student_attendance_menu(attendance_service, user):
    student_id = getattr(user, "student_id", None)
    if not student_id:
        print("❌ Cannot determine student ID.")
        return

    print("\n===== MY ATTENDANCE =====")
    data = attendance_service.view_attendance_by_student(student_id)
    if not data:
        print("No attendance data found.")
        return

    for attendance in data:
        print(attendance)
