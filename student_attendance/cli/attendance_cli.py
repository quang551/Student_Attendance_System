def _print_result(success, message):
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def attendance_menu(attendance_service, user=None, role=None):
    if role == "student":
        _student_attendance_menu(attendance_service, user)
        return

    while True:
        print("\n===== ATTENDANCE MENU =====")
        print("1. Mở session")
        print("2. Đóng session")
        print("3. Điểm danh")
        print("4. Xem điểm danh theo session")
        print("5. Xem điểm danh theo student")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()

        if choice == "1":
            session_id = input("Session ID: ").strip()
            _print_result(*attendance_service.open_session(session_id))

        elif choice == "2":
            session_id = input("Session ID: ").strip()
            _print_result(*attendance_service.close_session(session_id))

        elif choice == "3":
            attendance_id = input("Attendance ID: ").strip()
            session_id = input("Session ID: ").strip()
            student_id = input("Student ID: ").strip()
            print("1. Present | 2. Absent | 3. Late")
            status = input("Status: ").strip()
            if not status.isdigit():
                print("❌ Status không hợp lệ")
                continue
            _print_result(*attendance_service.mark_attendance(attendance_id, session_id, student_id, int(status)))

        elif choice == "4":
            session_id = input("Session ID: ").strip()
            data = attendance_service.view_attendance_by_session(session_id)
            if not data:
                print("Không có dữ liệu điểm danh.")
            for row in data:
                print(row)

        elif choice == "5":
            student_id = input("Student ID: ").strip()
            data = attendance_service.view_attendance_by_student(student_id)
            if not data:
                print("Không có dữ liệu điểm danh.")
            for attendance in data:
                print(attendance)

        elif choice == "0":
            break

        else:
            print("Lựa chọn không hợp lệ.")


def _student_attendance_menu(attendance_service, user):
    student_id = getattr(user, "student_id", None)
    if not student_id:
        print("❌ Không xác định được student_id.")
        return

    print("\n===== MY ATTENDANCE =====")
    data = attendance_service.view_attendance_by_student(student_id)
    if not data:
        print("Không có dữ liệu điểm danh.")
        return

    for attendance in data:
        print(attendance)
