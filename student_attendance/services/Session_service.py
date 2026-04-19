from models.session import Session

class SessionService:
    def __init__(self, session_repo, class_repo):
        self.session_repo = session_repo
        self.class_repo = class_repo

    #  thêm buổi học
    def create_session(self, session_id, class_id, day, start_time, end_time):
        if self.session_repo.find_by_id(session_id):
            print("Session already exists!")
            return False

        # check class tồn tại
        if not self.class_repo.find_by_id(class_id):
            print("Class not found!")
            return False

        session = Session(session_id, class_id, day, start_time, end_time)
        self.session_repo.add(session)
        print("Session created!")
        return True

    #  Xóa
    def delete_session(self, session_id):
        if self.session_repo.delete(session_id):
            print("Session deleted!")
            return True
        print("Session not found!")
        return False

    #  Sửa
    def update_session(self, session_id, day=None, start_time=None, end_time=None):
        s = self.session_repo.find_by_id(session_id)
        if not s:
            print("Session not found!")
            return False

        if day is not None:
            s.day = day
        if start_time is not None:
            s.start_time = start_time
        if end_time is not None:
            s.end_time = end_time

        print("Session updated!")
        return True