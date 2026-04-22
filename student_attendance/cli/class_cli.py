def _print_result(result):
    success = result[0]
    message = result[1]
    prefix = "✔" if success else "❌"
    print(f"{prefix} {message}")


def _print_classes(service):
    print("Available classes:")
    classes = service.list_classes()
    if not classes:
        print("No classes found.")
        return []

    for item in classes:
        print(item)
    return classes


def _print_courses(course_service):
    if not course_service:
        return []

    print("Available courses:")
    courses = course_service.list_courses()
    if not courses:
        print("No courses found.")
        return []

    for item in courses:
        print(item)
    return courses


def class_menu(service, course_service=None):
    while True:
        print("\n--- CLASS MENU ---")
        print("1. Create class")
        print("2. Update class")
        print("3. Delete class")
        print("4. View classes")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            _print_courses(course_service)
            cid = input("Class ID: ").strip()
            course_id = input("Course ID: ").strip()
            class_name = input("Class name: ").strip()
            _print_result(service.create_class(cid, course_id, class_name or None))

        elif choice == "2":
            _print_classes(service)
            cid = input("Class ID: ").strip()
            _print_courses(course_service)
            course_id = input("New course ID (Press Enter to keep current): ").strip()
            class_name = input("New class name (Press Enter to keep current): ").strip()
            _print_result(service.update_class(cid, course_id or None, class_name or None))

        elif choice == "3":
            _print_classes(service)
            cid = input("Class ID: ").strip()
            _print_result(service.delete_class(cid))

        elif choice == "4":
            classes = service.list_classes()
            if not classes:
                print("No classes found.")
            for c in classes:
                print(c)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
