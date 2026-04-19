def session_menu(service):
    while True:
        print("\n--- SESSION MENU ---")
        print("1. Tạo buổi học")
        print("2. Sửa buổi học")
        print("3. Xóa buổi học")
        print("4. Xem danh sách")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == "1":
            sid = input("Session ID: ")
            class_id = input("Class ID: ")
            date = input("Thứ: ")
            start_time = input("Giờ bắt đầu (HH:MM): ")
            end_time = input("Giờ kết thúc (HH:MM): ")

            service.create_session(sid, class_id, date, start_time, end_time)

        elif choice == "2":
            sid = input("Session ID: ")
            date = input("Thứ: ")
            start_time = input("Giờ bắt đầu (HH:MM): ")
            end_time = input("Giờ kết thúc (HH:MM): ")

            service.update_session(sid, date, start_time, end_time)

        elif choice == "3":
            sid = input("Session ID: ")
            service.delete_session(sid)

        elif choice == "4":
            for s in service.list_sessions():
                print(s.session_id, s.class_id, s.date, s.start_time, s.end_time)

        elif choice == "0":
            break