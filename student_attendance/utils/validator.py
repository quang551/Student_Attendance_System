from student_attendance.models.user import UserRole


def is_blank(value) -> bool:
    return value is None or str(value).strip() == ""


def normalize_role(role: str | None) -> str | None:
    if role is None:
        return None
    return str(role).strip().lower()


def is_valid_role(role: str | None) -> bool:
    if role is None:
        return False
    return normalize_role(role) in {item.value for item in UserRole}


def is_valid_email(email: str | None) -> bool:
    if is_blank(email):
        return False
    value = str(email).strip()
    return "@" in value and "." in value.split("@")[-1]
