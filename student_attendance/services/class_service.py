import sqlite3

from student_attendance.models.class_model import Class
from student_attendance.repositories.class_repo import ClassRepo
from student_attendance.repositories.user_repo import UserRepo


class ClassService:
    def __init__(self, class_repo=None, course_repo=None, user_repo=None):
        self.class_repo = class_repo or ClassRepo()
        self.course_repo = course_repo
        self.user_repo = user_repo or UserRepo()

    def create_class(self, class_id, course_id, class_name=None):
        if self.class_repo.find_by_id(class_id):
            return False, "Class already exists!", None
        if self.course_repo and not self.course_repo.find_by_id(course_id):
            return False, "Course not found!", None

        new_class = Class(class_id, class_name or class_id, course_id)
        return True, "Class created successfully!", self.class_repo.add(new_class)

    def delete_class(self, class_id):
        current = self.class_repo.find_by_id(class_id)
        if not current:
            return False, "Class not found!"

        students = self.class_repo.list_students(class_id)
        sessions = self.class_repo.list_sessions(class_id)

        problems = []
        if students:
            problems.append(f"{len(students)} student(s)")
        if sessions:
            problems.append(f"{len(sessions)} session(s)")

        if problems:
            return False, f"Cannot delete class because it still has: {', '.join(problems)}."

        try:
            self.class_repo.delete(class_id)
            return True, "Class deleted!"
        except sqlite3.IntegrityError:
            return False, "Cannot delete class because it is still referenced by other data."

    def update_class(self, class_id, course_id=None, class_name=None):
        current = self.class_repo.find_by_id(class_id)
        if not current:
            return False, "Class not found!", None
        if course_id and self.course_repo and not self.course_repo.find_by_id(course_id):
            return False, "Course not found!", None

        self.class_repo.update(class_id, new_course_id=course_id, new_class_name=class_name)
        return True, "Class updated!", self.class_repo.find_by_id(class_id)

    def list_classes(self):
        return self.class_repo.get_all()

    def list_classes_for_lecturer(self, lecturer_id):
        return self.class_repo.list_by_lecturer(lecturer_id)

    def list_classes_for_student(self, student_id):
        return self.class_repo.list_by_student(student_id)

    def list_students(self, class_id):
        current = self.class_repo.find_by_id(class_id)
        if not current:
            return False, "Class not found!", []
        return True, "OK", self.class_repo.list_students(class_id)

    def add_student(self, class_id, student_id, student_name=None):
        current = self.class_repo.find_by_id(class_id)
        if not current:
            return False, "Class not found!"

        student = self.user_repo.get_role_user("student", student_id)
        if not student:
            return False, "Student not found!"
        if self.class_repo.is_student_enrolled(class_id, student_id):
            return False, "Student already in class!"

        class_student_id = f"CS_{class_id}_{student_id}"
        self.class_repo.enroll_student(class_id, student_id, class_student_id)
        return True, "Student enrolled successfully!"

    def assign_lecturer(self, class_id, lecturer_id, lecturer_name=None):
        current = self.class_repo.find_by_id(class_id)
        if not current:
            return False, "Class not found!"

        lecturer = self.user_repo.get_role_user("lecturer", lecturer_id)
        if not lecturer:
            return False, "Lecturer not found!"

        self.class_repo.update(class_id, lecturer_id=lecturer_id)
        return True, "Lecturer assigned successfully!"
