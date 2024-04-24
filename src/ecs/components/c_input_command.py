from enum import Enum

class CInputCommand:
    def __init__(self, name:str, keys:list) -> None:
        self.name = name
        self.keys = keys
        self.phase = CommandPhase.NA

class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2