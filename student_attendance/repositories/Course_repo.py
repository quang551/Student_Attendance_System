class CourseRepo:
    def __init__(self):
        self.courses = []

    def add(self, course):
        if self.find_by_id(course.course_id):
            print("Course đã tồn tại!")
            return False
        self.courses.append(course)
        return True

    def get_all(self):
        return self.courses

    def find_by_id(self, course_id):
        for c in self.courses:
            if c.course_id == course_id:
                return c
        return None

    def delete(self, course_id):
        course = self.find_by_id(course_id)
        if course:
            self.courses.remove(course)
            return True
        return False

    def update(self, course_id, new_name=None, new_description=None):
        course = self.find_by_id(course_id)
        if course:
            if new_name is not None:
                course.name = new_name
            if new_description is not None:
                course.description = new_description
            return True
        return False

class SessionRepo:
    def __init__(self):
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def get_all(self):
        return self.sessions

    def find_by_id(self, session_id):
        for s in self.sessions:
            if s.session_id == session_id:
                return s
        return None

    def delete(self, session_id):
        self.sessions = [s for s in self.sessions if s.session_id != session_id]

    def update(self, session_id, new_date=None):
        session = self.find_by_id(session_id)
        if session:
            if new_date:
                session.date = new_date