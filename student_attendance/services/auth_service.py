from student_attendance.repositories.db import hash_password
from student_attendance.repositories.user_repo import UserRepo


def login(username, password):
    repo = UserRepo()
    return repo.authenticate(username, hash_password(password))