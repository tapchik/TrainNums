from dataclasses import dataclass

@dataclass
class Task:
    problem: str | None
    answer: str | None