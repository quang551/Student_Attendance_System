from models.session import Session
from repositories.class_repo import ClassRepo
from repositories.session_repo import SessionRepo


class SessionService:
    def __init__(self, session_repo=None, class_repo=None):
        self.session_repo = session_repo or SessionRepo()
        self.class_repo = class_repo or ClassRepo()

    def create_session(self, session_id, class_id):
        if self.session_repo.find_by_id(session_id):
            return False, "Session already exists!", None

        if not self.class_repo.find_by_id(class_id):
            return False, "Class not found!", None

        session = Session(
            session_id=session_id,
            class_id=class_id,
            start_time="",
            end_time="",
            is_open=False,
        )
        return True, "Session created successfully!", self.session_repo.add(session)

    def delete_session(self, session_id):
        if self.session_repo.delete(session_id):
            return True, "Session deleted!"
        return False, "Session not found!"

    def update_session(self, session_id, class_id=None):
        current = self.session_repo.find_by_id(session_id)
        if not current:
            return False, "Session not found!", None

        next_class_id = class_id or current.class_id
        if not self.class_repo.find_by_id(next_class_id):
            return False, "Class not found!", None

        self.session_repo.update(session_id, class_id=next_class_id)
        return True, "Session updated!", self.session_repo.find_by_id(session_id)

    def list_sessions(self):
        return self.session_repo.get_all()

    def list_sessions_for_class(self, class_id):
        return self.session_repo.list_by_class(class_id)
