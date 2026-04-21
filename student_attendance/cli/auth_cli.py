from services.auth_service import login


def login_cli():
    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = login(username, password)
    if user:
        print(f"✔ Login succesfully ({user.role})")
        return user

    print("❌ Invalid username or password")
    return None
