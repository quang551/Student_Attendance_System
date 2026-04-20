def _print_result(result):
    success = result[0]
    message = result[1]
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def class_menu(service):
    while True:
        print("\n--- CLASS MENU ---")
        print("1. Tạo lớp")
        print("2. Sửa lớp")
        print("3. Xóa lớp")
        print("4. Xem danh sách")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()

        if choice == "1":
            cid = input("Class ID: ").strip()
            course_id = input("Course ID: ").strip()
            class_name = input("Tên lớp: ").strip()
            _print_result(service.create_class(cid, course_id, class_name or None))

        elif choice == "2":
            cid = input("Class ID: ").strip()
            course_id = input("Course ID mới (Enter để giữ nguyên): ").strip()
            class_name = input("Tên lớp mới (Enter để giữ nguyên): ").strip()
            _print_result(service.update_class(cid, course_id or None, class_name or None))

        elif choice == "3":
            cid = input("Class ID: ").strip()
            _print_result(service.delete_class(cid))

        elif choice == "4":
            classes = service.list_classes()
            if not classes:
                print("Không có lớp nào.")
            for c in classes:
                print(c)

        elif choice == "0":
            break

        else:
            print("Lựa chọn không hợp lệ.")
