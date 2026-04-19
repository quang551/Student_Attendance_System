class ClassRepo:
    def __init__(self):
        self.classes = []

    def add(self, new_class):
        # check trùng ID
        if self.find_by_id(new_class.class_id):
            print("Class đã tồn tại!")
            return False
        self.classes.append(new_class)
        return True

    def get_all(self):
        return self.classes

    def find_by_id(self, class_id):
        for c in self.classes:
            if c.class_id == class_id:
                return c
        return None

    def delete(self, class_id):
        c = self.find_by_id(class_id)
        if c:
            self.classes.remove(c)
            return True
        return False

    def update(self, class_id, new_course_id=None):
        c = self.find_by_id(class_id)
        if c:
            if new_course_id is not None:
                c.course_id = new_course_id
            return True
        return False