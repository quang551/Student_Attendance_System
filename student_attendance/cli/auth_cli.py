from services.auth_service import login

def login_cli():
    print("\n=== LOGIN ===")

    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user:
        print(f"✔ Login thành công ({user.role})")
        return user
    else:
        print("❌ Sai tài khoản")
        return None