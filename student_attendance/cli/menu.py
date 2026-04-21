from cli.attendance_cli import attendance_menu
from cli.class_cli import class_menu
from cli.report_cli import report_menu


def _header(title: str):
    print("\n" + "=" * 52)
    print(f"   {title}")
    print("=" * 52)


def _inp(prompt: str) -> str:
    return input(f"{prompt}").strip()


def _pause():
    input("\nPress Enter to continue...")


def _print_result(result):
    success = result[0]
    message = result[1]
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def _do_logout(user):
    print(f"\nLogged out. Goodbye, {user.full_name}!")


def _print_users(user_service, actor, role=None):
    label = f"{role.title()}s" if role else "Users"
    print(f"Available {label}:")
    ok, _, users = user_service.list_users(actor, role=role)
    if not ok or not users:
        print("No users found.")
        return []

    for item in users:
        if role == "lecturer":
            role_id = getattr(item, "lecturer_id", "-")
            print(f"{role_id} | {item.full_name} | {item.username} | {item.email}")
        elif role == "student":
            role_id = getattr(item, "student_id", "-")
            print(f"{role_id} | {item.full_name} | {item.username} | {item.email}")
        elif role == "admin":
            role_id = getattr(item, "admin_id", "-")
            print(f"{role_id} | {item.full_name} | {item.username} | {item.email}")
        else:
            print(item)
    return users


def _print_courses(course_service):
    print("Available courses:")
    courses = course_service.list_courses()
    if not courses:
        print("No courses found.")
        return []

    for item in courses:
        print(item)
    return courses


def _print_classes(class_service):
    print("Available classes:")
    classes = class_service.list_classes()
    if not classes:
        print("No classes found.")
        return []

    for item in classes:
        print(item)
    return classes


def _print_sessions(session_service):
    print("Available sessions:")
    sessions = session_service.list_sessions()
    if not sessions:
        print("No sessions found.")
        return []

    for item in sessions:
        print(item)
    return sessions


def _print_lecturer_classes(class_service, lecturer_id):
    print("Available classes:")
    classes = class_service.list_classes_for_lecturer(lecturer_id)
    if not classes:
        print("No classes assigned.")
        return []

    for item in classes:
        print(item)
    return classes


def _manage_users(user, user_service):
    while True:
        _header("USER MANAGEMENT")
        print("1. Create user")
        print("2. Update user")
        print("3. Delete user")
        print("4. View users")
        print("0. Back")
        choice = _inp("Choose: ")

        if choice == "1":
            user_id = _inp("User ID: ")
            username = _inp("Username: ")
            full_name = _inp("Full name: ")
            email = _inp("Email: ")
            role = _inp("Role (admin/lecturer/student): ").lower()
            password = _inp("Password: ")
            role_id = _inp("Role ID (leave blank to auto-generate): ")
            _print_result(
                user_service.create_user(
                    user,
                    user_id,
                    username,
                    full_name,
                    email,
                    role,
                    password,
                    role_id or None,
                )
            )
            _pause()

        elif choice == "2":
            _print_users(user_service, user)
            user_id = _inp("User ID to update: ")
            username = _inp("New username (leave blank to keep current): ")
            full_name = _inp("New full name (leave blank to keep current): ")
            email = _inp("New email (leave blank to keep current): ")
            role = _inp("New role (leave blank to keep current): ")
            password = _inp("New password (leave blank to keep current): ")
            payload = {
                "username": username or None,
                "full_name": full_name or None,
                "email": email or None,
                "role": role or None,
                "password": password or None,
            }
            _print_result(user_service.update_user(user, user_id, **payload))
            _pause()

        elif choice == "3":
            _print_users(user_service, user)
            user_id = _inp("User ID to delete: ")
            _print_result(user_service.delete_user(user, user_id))
            _pause()

        elif choice == "4":
            ok, _, users = user_service.list_users(user)
            if ok:
                for item in users:
                    print(item)
            _pause()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
            _pause()


def _manage_courses(course_service):
    while True:
        _header("COURSE MANAGEMENT")
        print("1. Create course")
        print("2. Update course")
        print("3. Delete course")
        print("4. View courses")
        print("0. Back")
        choice = _inp("Choose: ")

        if choice == "1":
            _print_result(
                course_service.create_course(
                    _inp("Course ID: "),
                    _inp("Course name: "),
                    _inp("Description: "),
                )
            )
            _pause()

        elif choice == "2":
            _print_courses(course_service)
            _print_result(
                course_service.update_course(
                    _inp("Course ID: "),
                    _inp("New course name: ") or None,
                    _inp("New description: ") or None,
                )
            )
            _pause()

        elif choice == "3":
            _print_courses(course_service)
            _print_result(course_service.delete_course(_inp("Course ID: ")))
            _pause()

        elif choice == "4":
            courses = course_service.list_courses()
            if not courses:
                print("No courses found.")
            for item in courses:
                print(item)
            _pause()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
            _pause()


def _manage_sessions(session_service, class_service):
    while True:
        _header("SESSION MANAGEMENT")
        print("1. Create session")
        print("2. Update session")
        print("3. Delete session")
        print("4. View sessions")
        print("0. Back")
        choice = _inp("Choose: ")

        if choice == "1":
            _print_classes(class_service)
            sid = _inp("Session ID: ")
            class_id = _inp("Class ID: ")
            _print_result(session_service.create_session(sid, class_id))
            _pause()

        elif choice == "2":
            _print_sessions(session_service)
            sid = _inp("Session ID: ")
            _print_classes(class_service)
            class_id = _inp("New class ID (leave blank to keep current): ")
            _print_result(session_service.update_session(sid, class_id or None))
            _pause()

        elif choice == "3":
            _print_sessions(session_service)
            _print_result(session_service.delete_session(_inp("Session ID: ")))
            _pause()

        elif choice == "4":
            sessions = session_service.list_sessions()
            if not sessions:
                print("No sessions found.")
            for item in sessions:
                print(item)
            _pause()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
            _pause()


def _assign_lecturer(class_service, user_service, actor):
    _header("ASSIGN LECTURER")

    _print_classes(class_service)
    print()
    _print_users(user_service, actor, role="lecturer")

    class_id = _inp("Class ID: ")
    lecturer_id = _inp("Lecturer ID: ")
    _print_result(class_service.assign_lecturer(class_id, lecturer_id))


def _enroll_student(class_service, user_service, actor):
    _header("ENROLL STUDENT")

    _print_classes(class_service)
    print()
    _print_users(user_service, actor, role="student")

    class_id = _inp("Class ID: ")
    student_id = _inp("Student ID: ")
    _print_result(class_service.add_student(class_id, student_id))


def _show_reports(user, services):
    report_menu(
        services["report_service"],
        class_service=services["class_service"],
        user_service=services["user_service"],
        actor=user,
    )


def _menu_admin(user, services):
    while True:
        _header(f"ADMIN - {user.full_name}")
        print("1. Manage users")
        print("2. Manage courses")
        print("3. Manage classes")
        print("4. Manage sessions")
        print("5. Assign lecturer to class")
        print("6. Enroll student")
        print("7. View reports")
        print("0. Logout")
        choice = _inp("Choose: ")

        if choice == "1":
            _manage_users(user, services["user_service"])

        elif choice == "2":
            _manage_courses(services["course_service"])

        elif choice == "3":
            class_menu(services["class_service"], services["course_service"])

        elif choice == "4":
            _manage_sessions(services["session_service"], services["class_service"])

        elif choice == "5":
            _assign_lecturer(
                services["class_service"],
                services["user_service"],
                user,
            )
            _pause()

        elif choice == "6":
            _enroll_student(
                services["class_service"],
                services["user_service"],
                user,
            )
            _pause()

        elif choice == "7":
            _show_reports(user, services)

        elif choice == "0":
            _do_logout(user)
            break

        else:
            print("Invalid choice.")
            _pause()


def _menu_lecturer(user, services):
    lecturer_id = getattr(user, "lecturer_id", None)

    while True:
        _header(f"LECTURER - {user.full_name}")
        print("1. View assigned classes")
        print("2. View students in a class")
        print("3. View sessions by class")
        print("4. Attendance")
        print("5. View reports")
        print("0. Logout")
        choice = _inp("Choose: ")

        if choice == "1":
            _print_lecturer_classes(services["class_service"], lecturer_id)
            _pause()

        elif choice == "2":
            _print_lecturer_classes(services["class_service"], lecturer_id)
            class_id = _inp("Class ID: ")
            ok, message, students = services["class_service"].list_students(class_id)
            if not ok:
                print(f"❌ {message}")
            elif not students:
                print("No students found.")
            else:
                for student in students:
                    print(
                        f"{student['student_id']} | "
                        f"{student['full_name']} | "
                        f"{student['user_name']} | "
                        f"{student['email']}"
                    )
            _pause()

        elif choice == "3":
            _print_lecturer_classes(services["class_service"], lecturer_id)
            class_id = _inp("Class ID: ")
            sessions = services["session_service"].list_sessions_for_class(class_id)
            if not sessions:
                print("No sessions found.")
            for item in sessions:
                print(item)
            _pause()

        elif choice == "4":
            attendance_menu(
                services["attendance_service"],
                session_service=services["session_service"],
                class_service=services["class_service"],
                user=user,
                role="lecturer",
            )

        elif choice == "5":
            _show_reports(user, services)

        elif choice == "0":
            _do_logout(user)
            break

        else:
            print("Invalid choice.")
            _pause()


def _menu_student(user, services):
    student_id = getattr(user, "student_id", None)

    while True:
        _header(f"STUDENT - {user.full_name}")
        print("1. View my classes")
        print("2. View my attendance")
        print("0. Logout")
        choice = _inp("Choose: ")

        if choice == "1":
            classes = services["class_service"].list_classes_for_student(student_id)
            if not classes:
                print("You are not enrolled in any classes.")
            for item in classes:
                print(item)
            _pause()

        elif choice == "2":
            attendance_menu(
                services["attendance_service"],
                user=user,
                role="student",
            )
            _pause()

        elif choice == "0":
            _do_logout(user)
            break

        else:
            print("Invalid choice.")
            _pause()


_ROLE_HANDLER = {
    "admin": _menu_admin,
    "lecturer": _menu_lecturer,
    "student": _menu_student,
}


def show_menu(user, services):
    handler = _ROLE_HANDLER.get(user.role.lower())
    if not handler:
        print(f"Error: unsupported role '{user.role}'")
        return

    try:
        handler(user, services)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
