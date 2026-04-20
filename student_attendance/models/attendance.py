from dataclasses import dataclass
from enum import IntEnum


class AttendanceStatus(IntEnum):
    PRESENT = 1
    ABSENT = 2
    LATE = 3


@dataclass(slots=True)
class Attendance:
    attendance_id: str
    session_id: str
    student_id: str
    status: int
    recorded_at: str
    student_name: str | None = None
    class_name: str | None = None

    def mark_present(self):
        self.status = AttendanceStatus.PRESENT

    def mark_absent(self):
        self.status = AttendanceStatus.ABSENT

    def mark_late(self):
        self.status = AttendanceStatus.LATE

    def status_label(self):
        mapping = {
            1: "Present",
            2: "Absent",
            3: "Late",
        }
        return mapping.get(int(self.status), str(self.status))

    def __str__(self):
        student_display = self.student_name or self.student_id
        class_display = self.class_name or "-"
        return (
            f"[{self.attendance_id}] Student: {student_display} | "
            f"Class: {class_display} | Session: {self.session_id} | "
            f"Status: {self.status_label()} | Time: {self.recorded_at}"
        )
