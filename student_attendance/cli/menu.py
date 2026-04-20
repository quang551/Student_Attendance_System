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
    input("\nNhấn Enter để tiếp tục...")


def _print_result(result):
    success = result[0]
    message = result[1]
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def _do_logout(user):
    print(f"\nĐã đăng xuất. Tạm biệt {user.full_name}!")


def _manage_users(user, user_service):
    while True:
        _header("QUẢN LÝ NGƯỜI DÙNG")
        print("1. Tạo người dùng")
        print("2. Sửa người dùng")
        print("3. Xóa người dùng")
        print("4. Xem danh sách")
        print("0. Quay lại")
        choice = _inp("Chọn: ")

        if choice == "1":
            user_id = _inp("User ID: ")
            username = _inp("Username: ")
            full_name = _inp("Full Name: ")
            email = _inp("Email: ")
            role = _inp("Role (admin/lecturer/student): ").lower()
            password = _inp("Password: ")
            role_id = _inp("Role ID (Enter để tự sinh): ")
            _print_result(user_service.create_user(user, user_id, username, full_name, email, role, password, role_id or None))
            _pause()

        elif choice == "2":
            user_id = _inp("User ID cần sửa: ")
            username = _inp("Username mới (Enter để giữ nguyên): ")
            full_name = _inp("Full Name mới (Enter để giữ nguyên): ")
            email = _inp("Email mới (Enter để giữ nguyên): ")
            role = _inp("Role mới (Enter để giữ nguyên): ")
            password = _inp("Password mới (Enter để giữ nguyên): ")
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
            user_id = _inp("User ID cần xóa: ")
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
            print("Lựa chọn không hợp lệ.")
            _pause()


def _manage_courses(course_service):
    while True:
        _header("QUẢN LÝ KHÓA HỌC")
        print("1. Tạo khóa học")
        print("2. Sửa khóa học")
        print("3. Xóa khóa học")
        print("4. Xem danh sách")
        print("0. Quay lại")
        choice = _inp("Chọn: ")

        if choice == "1":
            _print_result(course_service.create_course(_inp("Course ID: "), _inp("Tên khóa học: "), _inp("Mô tả: ")))
            _pause()
        elif choice == "2":
            _print_result(course_service.update_course(_inp("Course ID: "), _inp("Tên mới: ") or None, _inp("Mô tả mới: ") or None))
            _pause()
        elif choice == "3":
            _print_result(course_service.delete_course(_inp("Course ID: ")))
            _pause()
        elif choice == "4":
            courses = course_service.list_courses()
            if not courses:
                print("Không có khóa học nào.")
            for item in courses:
                print(item)
            _pause()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")
            _pause()


def _manage_sessions(session_service):
    while True:
        _header("QUẢN LÝ BUỔI HỌC")
        print("1. Tạo buổi học")
        print("2. Sửa buổi học")
        print("3. Xóa buổi học")
        print("4. Xem danh sách")
        print("0. Quay lại")
        choice = _inp("Chọn: ")

        if choice == "1":
            sid = _inp("Session ID: ")
            class_id = _inp("Class ID: ")
            day = _inp("Ngày (YYYY-MM-DD): ")
            start_time = _inp("Giờ bắt đầu (HH:MM): ")
            end_time = _inp("Giờ kết thúc (HH:MM): ")
            _print_result(session_service.create_session(sid, class_id, day, start_time, end_time))
            _pause()
        elif choice == "2":
            sid = _inp("Session ID: ")
            day = _inp("Ngày mới (Enter để giữ nguyên): ")
            start_time = _inp("Giờ bắt đầu mới (Enter để giữ nguyên): ")
            end_time = _inp("Giờ kết thúc mới (Enter để giữ nguyên): ")
            _print_result(session_service.update_session(sid, day or None, start_time or None, end_time or None))
            _pause()
        elif choice == "3":
            _print_result(session_service.delete_session(_inp("Session ID: ")))
            _pause()
        elif choice == "4":
            sessions = session_service.list_sessions()
            if not sessions:
                print("Không có buổi học nào.")
            for item in sessions:
                print(item)
            _pause()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")
            _pause()


def _assign_lecturer(class_service):
    class_id = _inp("Class ID: ")
    lecturer_id = _inp("Lecturer ID: ")
    _print_result(class_service.assign_lecturer(class_id, lecturer_id))


def _enroll_student(class_service):
    class_id = _inp("Class ID: ")
    student_id = _inp("Student ID: ")
    _print_result(class_service.add_student(class_id, student_id))


def _menu_admin(user, services):
    while True:
        _header(f"ADMIN – {user.full_name}")
        print("1. Quản lý người dùng")
        print("2. Quản lý khóa học")
        print("3. Quản lý lớp học")
        print("4. Quản lý buổi học")
        print("5. Phân công giảng viên cho lớp")
        print("6. Ghi danh sinh viên")
        print("7. Xem báo cáo")
        print("0. Đăng xuất")
        choice = _inp("Chọn: ")

        if choice == "1":
            _manage_users(user, services["user_service"])
        elif choice == "2":
            _manage_courses(services["course_service"])
        elif choice == "3":
            class_menu(services["class_service"])
        elif choice == "4":
            _manage_sessions(services["session_service"])
        elif choice == "5":
            _assign_lecturer(services["class_service"])
            _pause()
        elif choice == "6":
            _enroll_student(services["class_service"])
            _pause()
        elif choice == "7":
            report_menu(services["report_service"])
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("Lựa chọn không hợp lệ.")
            _pause()


def _menu_lecturer(user, services):
    lecturer_id = getattr(user, "lecturer_id", None)
    while True:
        _header(f"LECTURER – {user.full_name}")
        print("1. Xem lớp được phân công")
        print("2. Xem danh sách sinh viên của lớp")
        print("3. Xem buổi học theo lớp")
        print("4. Điểm danh")
        print("5. Chỉnh sửa điểm danh")
        print("6. Xem báo cáo")
        print("0. Đăng xuất")
        choice = _inp("Chọn: ")

        if choice == "1":
            classes = services["class_service"].list_classes_for_lecturer(lecturer_id)
            if not classes:
                print("Không có lớp nào được phân công.")
            for item in classes:
                print(item)
            _pause()
        elif choice == "2":
            class_id = _inp("Class ID: ")
            ok, message, students = services["class_service"].list_students(class_id)
            if not ok:
                print(f"❌ {message}")
            elif not students:
                print("Không có sinh viên nào.")
            else:
                for student in students:
                    print(f"{student['student_id']} | {student['full_name']} | {student['user_name']} | {student['email']}")
            _pause()
        elif choice == "3":
            class_id = _inp("Class ID: ")
            sessions = services["session_service"].list_sessions_for_class(class_id)
            if not sessions:
                print("Không có buổi học nào.")
            for item in sessions:
                print(item)
            _pause()
        elif choice in {"4", "5"}:
            attendance_menu(services["attendance_service"], user=user, role="lecturer")
        elif choice == "6":
            report_menu(services["report_service"])
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("Lựa chọn không hợp lệ.")
            _pause()


def _menu_student(user, services):
    student_id = getattr(user, "student_id", None)
    while True:
        _header(f"STUDENT – {user.full_name}")
        print("1. Xem lớp học của tôi")
        print("2. Xem điểm danh của tôi")
        print("0. Đăng xuất")
        choice = _inp("Chọn: ")

        if choice == "1":
            classes = services["class_service"].list_classes_for_student(student_id)
            if not classes:
                print("Bạn chưa được ghi danh vào lớp nào.")
            for item in classes:
                print(item)
            _pause()
        elif choice == "2":
            attendance_menu(services["attendance_service"], user=user, role="student")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("Lựa chọn không hợp lệ.")
            _pause()


_ROLE_HANDLER = {
    "admin": _menu_admin,
    "lecturer": _menu_lecturer,
    "student": _menu_student,
}


def show_menu(user, services):
    handler = _ROLE_HANDLER.get(user.role.lower())
    if not handler:
        print(f"Lỗi: vai trò không được hỗ trợ '{user.role}'")
        return
    handler(user, services)
