class Course:
    def __init__(self, course_id, name, description):
        self.course_id = course_id
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.course_id} | {self.name} | {self.description}"