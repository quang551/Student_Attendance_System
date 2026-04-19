from services.attendance_service import *


def attendance_menu():
    while True:
        print("\n===== ATTENDANCE MENU =====")
        print("1. Tạo session")
        print("2. Mở session")
        print("3. Đóng session")
        print("4. Điểm danh")
        print("5. Xem điểm danh theo session")
        print("6. Xem điểm danh theo student")
        print("0. Thoát")

        choice = input("Chọn: ")

        if choice == "1":
            session_id = input("Session ID: ")
            class_id = input("Class ID: ")
            start = input("Start time: ")
            end = input("End time: ")
            create_session(session_id, class_id, start, end)
            print("✔ Tạo session thành công")

        elif choice == "2":
            session_id = input("Session ID: ")
            open_session(session_id)
            print("✔ Session đã mở")

        elif choice == "3":
            session_id = input("Session ID: ")
            close_session(session_id)
            print("✔ Session đã đóng")

        elif choice == "4":
            attendance_id = input("Attendance ID: ")
            session_id = input("Session ID: ")
            student_id = input("Student ID: ")

            print("1. Present | 2. Absent | 3. Late")
            status = int(input("Status: "))
            mark_attendance(attendance_id, session_id, student_id, status)

        elif choice == "5":
            session_id = input("Session ID: ")
            data = view_attendance_by_session(session_id)

            for row in data:
                print(row)

        elif choice == "6":
            student_id = input("Student ID: ")
            data = view_attendance_by_student(student_id)

            for attendance in data:
                print(attendance)

        elif choice == "0":
            break