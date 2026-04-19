from models.class_model import Class

class ClassService:
    def __init__(self, class_repo, course_repo):
        self.class_repo = class_repo
        self.course_repo = course_repo

    # 🏫 Tạo lớp
    def create_class(self, class_id, course_id):
        if self.class_repo.find_by_id(class_id):
            print("Class already exists!")
            return

        # ✅ check course tồn tại
        if not self.course_repo.find_by_id(course_id):
            print("Course not found!")
            return

        new_class = Class(class_id, course_id)
        self.class_repo.add(new_class)

    # ❌ Xóa lớp
    def delete_class(self, class_id):
        if not self.class_repo.find_by_id(class_id):
            print("Class not found!")
            return
        self.class_repo.delete(class_id)

    # ✏️ Sửa lớp
    def update_class(self, class_id, course_id):
        c = self.class_repo.find_by_id(class_id)
        if not c:
            print("Class not found!")
            return

        if not self.course_repo.find_by_id(course_id):
            print("Course not found!")
            return

        self.class_repo.update(class_id, course_id)

 
    # 👨‍🎓 Thêm sinh viên
    def add_student(self, class_id, student):
        c = self.class_repo.find_by_id(class_id)
        if not c:
            print("Class not found!")
            return

        if student in c.students:
            print("Student already in class!")
            return

        c.students.append(student)

    # 👨‍🏫 Gán giảng viên
    def assign_lecturer(self, class_id, lecturer):
        c = self.class_repo.find_by_id(class_id)
        if not c:
            print("Class not found!")
            return

        if c.lecturer:
            print("Class already has a lecturer!")
            return

        c.lecturer = lecturer