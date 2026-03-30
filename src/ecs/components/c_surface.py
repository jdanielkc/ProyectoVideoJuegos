import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Vector2) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
