import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path: str) -> None:
        if path not in self._fonts:
            self._fonts[path] = pygame.font.Font(path, 12)
        return self._fonts[path]