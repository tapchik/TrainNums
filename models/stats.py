from dataclasses import dataclass

@dataclass
class Stats:
    correct: int
    incorrect: int
    skipped: int