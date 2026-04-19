from models.course import Course

class CourseService:
    def __init__(self, course_repo):
        self.course_repo = course_repo

    # 📚 Tạo khóa học
    def create_course(self, course_id, name, description):
        if self.course_repo.find_by_id(course_id):
            print("Course already exists!")
            return False

        course = Course(course_id, name, description)
        self.course_repo.add(course)
        print("Course created successfully!")
        return True

    # ❌ Xóa khóa học
    def delete_course(self, course_id):
        if self.course_repo.delete(course_id):
            print("Course deleted!")
            return True
        print("Course not found!")
        return False

    # ✏️ Sửa khóa học
    def update_course(self, course_id, name=None, description=None):
        if self.course_repo.update(course_id, name, description):
            print("Course updated!")
            return True
        print("Course not found!")
        return False

    # 📋 Xem danh sách
    def list_courses(self):
        courses = self.course_repo.get_all()
        if not courses:
            print("No courses available!")
        return courses

    # 🔍 Tìm theo ID
    def find_course(self, course_id):
        course = self.course_repo.find_by_id(course_id)
        if not course:
            print("Course not found!")
            return None
        return course