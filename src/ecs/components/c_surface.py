import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Vector2) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)

    @classmethod
    def from_surface(cls, surf: pygame.Surface):
        instance = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        instance.surf = surf
        return instance
