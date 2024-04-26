from enum import Enum

class CShieldState():
    def __init__(self) -> None:
        self.state = ShieldState.PROTECT


class ShieldState(Enum):
    PROTECT = 0