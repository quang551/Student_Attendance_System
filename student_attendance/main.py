from repositories.db import init_db

if __name__ == "__main__":
    init_db()


from cli.attendance_cli import attendance_menu

if __name__ == "__main__":
    attendance_menu()
