from dataclasses import dataclass

@dataclass
class user_settings():
    addition: bool
    subtraction: bool
    multiplication: bool
    division: bool
    max_sum: bool
    max_factor: bool