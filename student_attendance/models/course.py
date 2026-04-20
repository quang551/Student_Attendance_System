from dataclasses import dataclass


@dataclass(slots=True)
class Course:
    course_id: str
    name: str
    description: str

    def __str__(self):
        return f"{self.course_id} | {self.name} | {self.description}"