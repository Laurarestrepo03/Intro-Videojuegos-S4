from enum import Enum
import pygame

class CTagEnemy():
    def __init__(self, type:int, origin:pygame.Vector2) -> None:
        self.type = type
        self.origin = origin

class EnemyType(Enum):
    ASTEROID = 0
    HUNTER = 1