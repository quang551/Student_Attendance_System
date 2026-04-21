def report_menu(service):
    while True:
        print("\n=== REPORT ===")
        print("1. By class")
        print("2. By student")
        print("0. Back")

        choice = input("Choose: ").strip()
        if choice == "1":
            class_id = input("Enter class_id: ").strip()
            _print_report(service.report_by_class(class_id))
        elif choice == "2":
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
