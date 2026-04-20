from dataclasses import dataclass


@dataclass(slots=True)
class Session:
    session_id: str
    class_id: str
    start_time: str
    end_time: str
    is_open: bool = False

    @property
    def date(self) -> str:
        return self.start_time.split(" ", 1)[0] if " " in self.start_time else self.start_time

    def __str__(self):
        state = "open" if self.is_open else "closed"
        return f"{self.session_id} | {self.class_id} | {self.start_time}-{self.end_time} | {state}"