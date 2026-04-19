class Attendance:
    def __init__(self, attendance_id, session_id, student_id, status, recorded_at):
        self.attendance_id = attendance_id
        self.session_id = session_id
        self.student_id = student_id
        self.status = status
        self.recorded_at = recorded_at

    def __str__(self):
        return f"[{self.attendance_id}] Student: {self.student_id} | Session: {self.session_id} | Status: {self.status} | Time: {self.recorded_at}"