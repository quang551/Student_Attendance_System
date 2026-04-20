from models.user import User
from repositories.db import hash_password
from repositories.user_repo import UserRepo
from utils.validator import is_blank, is_valid_email, is_valid_role, normalize_role


class UserService:
    def __init__(self, user_repo=None):
        self.user_repo = user_repo or UserRepo()

    def create_user(self, actor, user_id, username, full_name, email, role, password, role_id=None):
        if not self._is_admin(actor):
            return False, "Permission denied", None
        if is_blank(user_id) or is_blank(username) or is_blank(full_name) or is_blank(password):
            return False, "Required fields must not be empty", None
        role = normalize_role(role)
        if not is_valid_role(role):
            return False, "Invalid role", None
        if not is_valid_email(email):
            return False, "Invalid email", None
        if self.user_repo.get_by_id(user_id) or self.user_repo.get_by_username(username):
            return False, "User already exists", None

        user = User(
            user_id=user_id,
            username=username,
            full_name=full_name,
            email=email,
            role=role,
            password=hash_password(password),
        )
        created = self.user_repo.create(user, role_id=role_id)
        return True, "User created successfully", created

    def update_user(self, actor, user_id, **fields):
        if not self._is_admin(actor):
            return False, "Permission denied", None

        if "email" in fields and fields["email"] is not None and not is_valid_email(fields["email"]):
            return False, "Invalid email", None
        if "role" in fields and fields["role"] is not None:
            fields["role"] = normalize_role(fields["role"])
            if not is_valid_role(fields["role"]):
                return False, "Invalid role", None
        if "password" in fields and fields["password"] is not None:
            fields["password"] = hash_password(fields["password"])

        updated = self.user_repo.update(user_id, **fields)
        if not updated:
            return False, "User not found", None
        return True, "User updated successfully", updated

    def delete_user(self, actor, user_id):
        if not self._is_admin(actor):
            return False, "Permission denied"
        if self.user_repo.delete(user_id):
            return True, "User deleted successfully"
        return False, "User not found"

    def list_users(self, actor, role=None):
        if not self._is_admin(actor):
            return False, "Permission denied", []
        normalized_role = normalize_role(role) if role else None
        return True, "OK", self.user_repo.list_all(normalized_role)

    def _is_admin(self, actor):
        return actor and getattr(actor, "role", None) == "admin"
