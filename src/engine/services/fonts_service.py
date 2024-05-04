import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path: str, size:int) -> None:
        font_key = path + "-" + str(size)
        if font_key not in self._fonts:
            self._fonts[font_key] = pygame.font.Font(path, size)
        return self._fonts[font_key]