from dataclasses import dataclass


@dataclass(slots=True)
class Class:
    class_id: str
    class_name: str
    course_id: str
    lecturer_id: str | None = None
    course_name: str | None = None
    lecturer_name: str | None = None

    def __str__(self):
        course_display = self.course_name or self.course_id
        lecturer_display = self.lecturer_name or self.lecturer_id or "-"
        return f"{self.class_id} | {self.class_name} | course={course_display} | lecturer={lecturer_display}"
