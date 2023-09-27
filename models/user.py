from dataclasses import dataclass
from models import Task
from models import Settings
from models import Stats

@dataclass
class User:
    id: str
    state: int
    task: Task
    settings: Settings
    stats: Stats