class Session:
    def __init__(self, session_id, class_id, day, start_time, end_time):
        self.session_id = session_id
        self.class_id = class_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.session_id} | {self.class_id} | {self.day} | {self.start_time}-{self.end_time}"