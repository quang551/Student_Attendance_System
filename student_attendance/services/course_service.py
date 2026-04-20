from models.course import Course
from repositories.Course_repo import CourseRepo


class CourseService:
    def __init__(self, course_repo=None):
        self.course_repo = course_repo or CourseRepo()

    def create_course(self, course_id, name, description):
        if self.course_repo.find_by_id(course_id):
            return False, "Course already exists!", None

        course = Course(course_id, name, description)
        return True, "Course created successfully!", self.course_repo.add(course)

    def delete_course(self, course_id):
        if self.course_repo.delete(course_id):
            return True, "Course deleted!"
        return False, "Course not found!"

    def update_course(self, course_id, name=None, description=None):
        if self.course_repo.update(course_id, name, description):
            return True, "Course updated!", self.course_repo.find_by_id(course_id)
        return False, "Course not found!", None

    def list_courses(self):
        return self.course_repo.get_all()

    def find_course(self, course_id):
        return self.course_repo.find_by_id(course_id)
