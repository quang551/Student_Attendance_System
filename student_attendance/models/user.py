from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    LECTURER = "lecturer"
    STUDENT = "student"


@dataclass(slots=True)
class User:
    user_id: str
    username: str
    full_name: str
    email: str
    role: str
    password: str

    def login(self) -> bool:
        return True

    def logout(self) -> bool:
        return True

    def __str__(self):
        return f"{self.user_id} | {self.username} | {self.full_name} | {self.email} | {self.role}"


@dataclass(slots=True)
class Admin(User):
    admin_id: str


@dataclass(slots=True)
class Lecturer(User):
    lecturer_id: str


@dataclass(slots=True)
class Student(User):
    student_id: str