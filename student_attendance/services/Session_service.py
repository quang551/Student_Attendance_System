from models.session import Session
from repositories.class_repo import ClassRepo
from repositories.session_repo import SessionRepo


class SessionService:
    def __init__(self, session_repo=None, class_repo=None):
        self.session_repo = session_repo or SessionRepo()
        self.class_repo = class_repo or ClassRepo()

    def create_session(self, session_id, class_id, day, start_time, end_time):
        if self.session_repo.find_by_id(session_id):
            return False, "Session already exists!", None
        if not self.class_repo.find_by_id(class_id):
            return False, "Class not found!", None

        start_value = f"{day} {start_time}".strip()
        end_value = f"{day} {end_time}".strip()
        session = Session(session_id, class_id, start_value, end_value, False)
        return True, "Session created!", self.session_repo.add(session)

    def delete_session(self, session_id):
        if self.session_repo.delete(session_id):
            return True, "Session deleted!"
        return False, "Session not found!"

    def update_session(self, session_id, day=None, start_time=None, end_time=None):
        current = self.session_repo.find_by_id(session_id)
        if not current:
            return False, "Session not found!", None

        next_day = day or current.date
        next_start = start_time or current.start_time.split(" ", 1)[-1]
        next_end = end_time or current.end_time.split(" ", 1)[-1]
        self.session_repo.update(session_id, start_time=f"{next_day} {next_start}", end_time=f"{next_day} {next_end}")
        return True, "Session updated!", self.session_repo.find_by_id(session_id)

    def list_sessions(self):
        return self.session_repo.get_all()

    def list_sessions_for_class(self, class_id):
        return self.session_repo.list_by_class(class_id)
