def course_menu(service):
    while True:
        print("\n--- COURSE MENU ---")
        print("1. Add course")
        print("2. Update course")
        print("3. Delete course")
        print("4. View courses")
        print("0. Back")

        choice = input("Choose: ")

        if choice == "1":
            cid = input("ID: ")
            name = input("Name: ")
            desc = input("Description: ")

            service.create_course(cid, name, desc)

        elif choice == "2":
            cid = input("ID: ")
            name = input("New name: ")
            desc = input("New description: ")

            service.update_course(cid, name, desc)

        elif choice == "3":
            cid = input("ID: ")
            service.delete_course(cid)

        elif choice == "4":
            for c in service.list_courses():
                print(c)

        elif choice == "0":
            break