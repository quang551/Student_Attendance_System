from services.class_service import *
def class_menu(service):
    while True:
        print("\n--- CLASS MENU ---")
        print("1. Tạo lớp")
        print("2. Sửa lớp")
        print("3. Xóa lớp")
        print("4. Xem danh sách")
        print("5. Thêm sinh viên")
        print("6. Gán giảng viên")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == "1":
            cid = input("Class ID: ")
            course_id = input("Course ID: ")
            service.create_class(cid, course_id)

        elif choice == "2":
            cid = input("Class ID: ")
            course_id = input("Course ID mới: ")
            service.update_class(cid, course_id)

        elif choice == "3":
            cid = input("Class ID: ")
            service.delete_class(cid)

        elif choice == "4":
            for c in service.list_classes():
                print(c.class_id, c.course_id)

        elif choice == "5":
            cid = input("Class ID: ")
            student_id = input("Student ID: ")
            student_name = input("Tên sinh viên: ")
            service.add_student(cid, student_id, student_name)

        elif choice == "6":
            cid = input("Class ID: ")
            lecturer_id = input("Lecturer ID: ")
            lecturer_name = input("Tên giảng viên: ")
            service.assign_lecturer(cid, lecturer_id, lecturer_name)

        elif choice == "0":
            break