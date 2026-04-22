from dataclasses import dataclass


@dataclass(slots=True)
class ClassStudent:
    class_student_id: str
    class_id: str
    student_id: str