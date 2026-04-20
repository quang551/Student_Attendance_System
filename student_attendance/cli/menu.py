"""
cli/menu.py – Role-based CLI navigation

Valid roles (users.role):
  admin=1 | lecturer=2 | student=3


"""


import hashlib
import getpass



# UI Helpers

def _header(title: str):
    print("\n" + "=" * 52)
    print(f"   {title}")
    print("=" * 52)


def _inp(prompt: str) -> str:
    return input(f"  {prompt}").strip()


def _pause():
    input("\n  Nhấn Enter để tiếp tục...")


def _opts(options: list[tuple[str, str]]):
    print()
    for key, label in options:
        print(f"  [{key}] {label}")
    print()



# Security – Password Hashing


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()



# Authentication


def _do_login() -> dict | None:
    _header("ĐĂNG NHẬP – Hệ thống điểm danh học sinh")

    username = _inp(" Tên người dùng:")
    password = getpass.getpass("  Mật khẩu: ")

    # ===== DỮ LIỆU MÔ PHỎNG (xóa bỏ khi mô-đun xác thực sẵn sàng) =====
    _MOCK_USERS = {
        "admin01": {
            "password": "admin123",
            "role": "admin",
            "full_name": "Administrator",
            "user_id": "U001",
        },
        "lec01": {
            "password": "lecturer123",
            "role": "lecturer",
            "full_name": "Nguyen Thanh Tung",
            "user_id": "U002",
        },
        "stu01": {
            "password": "student123",
            "role": "student",
            "full_name": "Nguyen Van An",
            "user_id": "U003",
        },
    }

    info = _MOCK_USERS.get(username)

    if info and info["password"] == password:
        print("\n  ✓ Đăng nhập thành công!")
        print(f"  Chào mừng, {info['full_name']} ({info['role']})")
        return {k: v for k, v in info.items() if k != "password"}

    print("\n  ✗ Tên người dùng hoặc mật khẩu không hợp lệ.")
    return None


def _do_logout(user: dict):
    print(f"\n  Đã đăng xuất. Tạm biệt! {user['full_name']}!")



# Admin Menu


def _menu_admin(user: dict):
    opts = [
        ("1", "Quản lý người dùng"),
        ("2", "Quản lý các khóa học và lớp học"),
        ("3", "Quản lý buổi học"),
        ("4", "Phân công giảng viên cho lớp học"),
        ("5", "Ghi danh sinh viên"),
        ("6", "Xem báo cáo"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"ADMIN – {user['full_name']}")
        _opts(opts)
        choice = _inp(" Chọn tùy chọn: ")

        if choice == "1":
            print("\n  → Chức năng quản lý người dùng chưa sẵn sàng.")
            _pause()
        elif choice == "2":
            print("\n  → Công tác quản lý lớp học chưa sẵn sàng.")
            _pause()
        elif choice == "3":
            print("\n  → Chức năng quản lý phiên chưa sẵn sàng.")
            _pause()
        elif choice == "4":
            print("\n  → Giảng viên được chỉ định chưa sẵn sàng.")
            _pause()
        elif choice == "5":
            print("\n  → Ghi danh những sinh viên chưa sẵn sàng.")
            _pause()
        elif choice == "6":
            print("\n  → Báo cáo chưa sẵn sàng.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Tùy chọn không hợp lệ!")
            _pause()


# Lecturer Menu


def _menu_lecturer(user: dict):
    opts = [
        ("1", "Xem các khóa học và lớp học"),
        ("2", "Xem danh sách sinh viên"),
        ("3", "Xem buỏi học"),
        ("4", "Tham gia điểm danh"),
        ("5", "Chỉnh sửa điểm danh"),
        ("6", "Xem báo cáo"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"LECTURER – {user['full_name']}")
        _opts(opts)
        choice = _inp("Chọn tùy chọn: ")

        if choice == "1":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "2":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "3":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "4":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "5":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "6":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Tùy chọn không hợp lệ!")
            _pause()


# Student Menu


def _menu_student(user: dict):
    opts = [
        ("1", "Xem lớp học của tôi"),
        ("2", "View My Attendance"),
        ("0", "Đăng xuất"),
    ]

    while True:
        _header(f"STUDENT – {user['full_name']}")
        _opts(opts)
        choice = _inp("Chọn tùy chọn:")

        if choice == "1":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "2":
            print("\n  → Chưa sẵn sàng.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Tùy chọn không hợp lệ!")
            _pause()


# Role Router


_ROLE_HANDLER = {
    "admin": _menu_admin,
    "lecturer": _menu_lecturer,
    "student": _menu_student,
}



# Main Menu Class


class Menu:
    MAX_ATTEMPTS = 3

    def run(self):
        while True:
            user = self._login_loop()
            if user is None:
                print("\n Tạm biệt!\n")
                break

            role = user.get("role", "").lower()
            handler = _ROLE_HANDLER.get(role)

            if handler:
                handler(user)
            else:
                print(f"\n  LỖI: Vai trò không được hỗ trợ '{role}'")

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
                print("\n  Quá nhiều lần thất bại.")

        return None
