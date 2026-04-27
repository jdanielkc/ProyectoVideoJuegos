import pygame


class CUiHeart:
    def __init__(self, index: int, original_area: pygame.Rect) -> None:
        self.index = index
        self.original_area = original_area.copy()
