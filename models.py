from dataclasses import dataclass

@dataclass
class Task:
    problem: str | None
    answer: str | None

@dataclass
class Settings:
    addition: bool
    subtraction: bool
    multiplication: bool
    division: bool
    max_sum: int
    max_factor: int

@dataclass
class Stats:
    correct: int
    incorrect: int
    skipped: int

@dataclass
class User:
    id: str
    state: int
    task: Task
    settings: Settings
    stats: Stats
