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
    input("\n  Press Enter to continue...")


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
    _header("LOGIN – Student Attendance System")

    username = _inp("Username: ")
    password = getpass.getpass("  Password: ")

    # ===== MOCK DATA (remove when auth module is ready) =====
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
        print("\n  ✓ Login successful!")
        print(f"  Welcome, {info['full_name']} ({info['role']})")
        return {k: v for k, v in info.items() if k != "password"}

    print("\n  ✗ Invalid username or password.")
    return None


def _do_logout(user: dict):
    print(f"\n  Logged out. Goodbye, {user['full_name']}!")



# Admin Menu


def _menu_admin(user: dict):
    opts = [
        ("1", "Manage Users"),
        ("2", "Manage Courses & Classes"),
        ("3", "Manage Sessions"),
        ("4", "Assign Lecturer to Class"),
        ("5", "Enroll Students"),
        ("6", "View Reports"),
        ("0", "Logout"),
    ]

    while True:
        _header(f"ADMIN – {user['full_name']}")
        _opts(opts)
        choice = _inp("Select option: ")

        if choice == "1":
            print("\n  → User management not ready.")
            _pause()
        elif choice == "2":
            print("\n  → Class management not ready.")
            _pause()
        elif choice == "3":
            print("\n  → Session management not ready.")
            _pause()
        elif choice == "4":
            print("\n  → Assign lecturer not ready.")
            _pause()
        elif choice == "5":
            print("\n  → Enroll students not ready.")
            _pause()
        elif choice == "6":
            print("\n  → Reports not ready.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Invalid option!")
            _pause()


# Lecturer Menu


def _menu_lecturer(user: dict):
    opts = [
        ("1", "View Courses & Classes"),
        ("2", "View Student List"),
        ("3", "View Sessions"),
        ("4", "Take Attendance"),
        ("5", "Edit Attendance"),
        ("6", "View Reports"),
        ("0", "Logout"),
    ]

    while True:
        _header(f"LECTURER – {user['full_name']}")
        _opts(opts)
        choice = _inp("Select option: ")

        if choice == "1":
            print("\n  → Not ready.")
            _pause()
        elif choice == "2":
            print("\n  → Not ready.")
            _pause()
        elif choice == "3":
            print("\n  → Not ready.")
            _pause()
        elif choice == "4":
            print("\n  → Not ready.")
            _pause()
        elif choice == "5":
            print("\n  → Not ready.")
            _pause()
        elif choice == "6":
            print("\n  → Not ready.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Invalid option!")
            _pause()


# Student Menu


def _menu_student(user: dict):
    opts = [
        ("1", "View My Classes"),
        ("2", "View My Attendance"),
        ("0", "Logout"),
    ]

    while True:
        _header(f"STUDENT – {user['full_name']}")
        _opts(opts)
        choice = _inp("Select option: ")

        if choice == "1":
            print("\n  → Not ready.")
            _pause()
        elif choice == "2":
            print("\n  → Not ready.")
            _pause()
        elif choice == "0":
            _do_logout(user)
            break
        else:
            print("\n  Invalid option!")
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
                print("\n  Goodbye!\n")
                break

            role = user.get("role", "").lower()
            handler = _ROLE_HANDLER.get(role)

            if handler:
                handler(user)
            else:
                print(f"\n  ERROR: Unsupported role '{role}'")

            again = _inp("\nLogin again? (y/n): ").lower()
            if again != "y":
                print("\n  Goodbye!\n")
                break

    def _login_loop(self) -> dict | None:
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            user = _do_login()
            if user:
                return user

            remaining = self.MAX_ATTEMPTS - attempt
            if remaining > 0:
                print(f"\n  Attempts remaining: {remaining}")
            else:
                print("\n  Too many failed attempts.")

        return None
