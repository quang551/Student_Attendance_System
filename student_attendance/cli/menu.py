def _do_login() -> dict | None:
    _header("ĐĂNG NHẬP – Hệ thống điểm danh sinh viên")

    username = _inp("Tên đăng nhập: ")
    password = getpass.getpass("  Mật khẩu: ")

    _MOCK_USERS = {
        "admin01": {
            "password": "admin123",
            "role": "admin",
            "full_name": "Quản trị viên",
            "user_id": "U001",
        },
        "lec01": {
            "password": "lecturer123",
            "role": "lecturer",
            "full_name": "Nguyễn Thanh Tùng",
            "user_id": "U002",
        },
        "stu01": {
            "password": "student123",
            "role": "student",
            "full_name": "Nguyễn Văn An",
            "user_id": "U003",
        },
    }

    info = _MOCK_USERS.get(username)

    if info and info["password"] == password:
        print("\n  ✓ Đăng nhập thành công!")
        print(f"  Xin chào, {info['full_name']} ({info['role']})")
        return {k: v for k, v in info.items() if k != "password"}

    print("\n  ✗ Sai tên đăng nhập hoặc mật khẩu.")
    return None


def _do_logout(user: dict):
    print(f"\n  Đã đăng xuất. Tạm biệt, {user['full_name']}!")


def _menu_admin(user: dict):
    opts = [
        ("1", "Quản lý người dùng"),
        ("2", "Quản lý khóa học & lớp học"),
        ("3", "Quản lý buổi học"),
        ("4", "Phân công giảng viên"),
        ("5", "Ghi danh sinh viên"),
        ("6", "Xem báo cáo"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"QUẢN TRỊ – {user['full_name']}")
        _opts(opts)
        choice = _inp("Chọn chức năng: ")

        if choice == "1":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "2":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "3":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "4":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "5":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "6":
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Lựa chọn không hợp lệ!")
            _pause()


def _menu_lecturer(user: dict):
    opts = [
        ("1", "Xem khóa học & lớp học"),
        ("2", "Xem danh sách sinh viên"),
        ("3", "Xem buổi học"),
        ("4", "Điểm danh"),
        ("5", "Chỉnh sửa điểm danh"),
        ("6", "Xem báo cáo"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"GIẢNG VIÊN – {user['full_name']}")
        _opts(opts)
        choice = _inp("Chọn chức năng: ")

        if choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()


def _menu_student(user: dict):
    opts = [
        ("1", "Xem lớp học của tôi"),
        ("2", "Xem điểm danh của tôi"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"SINH VIÊN – {user['full_name']}")
        _opts(opts)
        choice = _inp("Chọn chức năng: ")

        if choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  → Chức năng chưa sẵn sàng.")
            _pause()


class Menu:
    MAX_ATTEMPTS = 3

    def run(self):
        while True:
            user = self._login_loop()
            if user is None:
                print("\n  Tạm biệt!\n")
                break

            role = user.get("role", "").lower()
            handler = _ROLE_HANDLER.get(role)

            if handler:
                handler(user)
            else:
                print(f"\n  LỖI: Vai trò không hỗ trợ '{role}'")

            again = _inp("\nĐăng nhập lại? (y/n): ").lower()
            if again != "y":
                print("\n  Tạm biệt!\n")
                break

    def _login_loop(self) -> dict | None:
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            user = _do_login()
            if user:
                return user

            remaining = self.MAX_ATTEMPTS - attempt
            if remaining > 0:
                print(f"\n  Số lần thử còn lại: {remaining}")
            else:
                print("\n  Quá số lần đăng nhập cho phép.")

        return None
