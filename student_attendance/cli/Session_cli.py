def session_menu(service):
    while True:
        print("\n--- SESSION MENU ---")
        print("1. Create session")
        print("2. Update session")
        print("3. Delete session")
        print("4. View sessions")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            sid = input("Session ID: ").strip()
            class_id = input("Class ID: ").strip()

            result = service.create_session(sid, class_id)
            print(result)

        elif choice == "2":
            sid = input("Session ID: ").strip()
            class_id = input("New class ID (leave blank to keep current): ").strip()

            result = service.update_session(
                sid,
                class_id or None,
            )
            print(result)

        elif choice == "3":
            sid = input("Session ID: ").strip()
            result = service.delete_session(sid)
            print(result)

        elif choice == "4":
            sessions = service.list_sessions()
            if not sessions:
                print("No sessions found.")
            else:
                print("\nSession ID | Class ID | Start Time | End Time | Status")
                for s in sessions:
                    status = "OPEN" if s.is_open else "CLOSED"
                    print(
                        f"{s.session_id} | "
                        f"{s.class_id} | "
                        f"{s.start_time or '-'} | "
                        f"{s.end_time or '-'} | "
                        f"{status}"
                    )

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
