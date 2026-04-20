from dataclasses import dataclass


@dataclass(slots=True)
class Class:
    class_id: str
    class_name: str
    course_id: str
    lecturer_id: str | None = None

    def __str__(self):
        lecturer = self.lecturer_id or "-"
        return f"{self.class_id} | {self.class_name} | course={self.course_id} | lecturer={lecturer}"