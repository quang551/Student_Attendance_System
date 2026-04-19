def course_menu(service):
    while True:
        print("\n--- COURSE MENU ---")
        print("1. Thêm khóa học")
        print("2. Sửa khóa học")
        print("3. Xóa khóa học")
        print("4. Xem danh sách")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == "1":
            cid = input("ID: ")
            name = input("Tên: ")
            desc = input("Mô tả: ")

            service.create_course(cid, name, desc)

        elif choice == "2":
            cid = input("ID: ")
            name = input("Tên mới: ")
            desc = input("Mô tả mới: ")

            service.update_course(cid, name, desc)

        elif choice == "3":
            cid = input("ID: ")
            service.delete_course(cid)

        elif choice == "4":
            for c in service.list_courses():
                print(c)

        elif choice == "0":
            break