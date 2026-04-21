def _print_classes(class_service):
    if not class_service:
        return

    classes = class_service.list_classes()
    print("\n===== CLASS LIST =====")
    if not classes:
        print("No classes found.")
        return

    for item in classes:
        print(item)


def _print_students(user_service, actor):
    if not user_service or not actor:
        return

    ok, _, students = user_service.list_users(actor, role="student")
    print("\n===== STUDENT LIST =====")
    if not ok or not students:
        print("No students found.")
        return

    for student in students:
        student_id = getattr(student, "student_id", "-")
        print(f"{student_id} | {student.full_name} | {student.username} | {student.email}")


def report_menu(service, class_service=None, user_service=None, actor=None):
    while True:
        print("\n=== REPORT ===")
        print("1. By class")
        print("2. By student")
        print("0. Back")

        choice = input("Choose: ").strip()
        if choice == "1":
            _print_classes(class_service)
            class_id = input("Enter class_id: ").strip()
            _print_report(service.report_by_class(class_id))
        elif choice == "2":
            _print_students(user_service, actor)
            student_id = input("Enter student_id: ").strip()
            _print_report(service.report_by_student(student_id))
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def _print_report(report):
    print(f"Total: {report['total']}")
    print(f"Present: {report['present']}")
    print(f"Absent: {report['absent']}")
    print(f"Late: {report['late']}")
    print(f"Attendance Rate: {report['rate']}%")
