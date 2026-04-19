import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Vector2) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surf: pygame.Surface):
        instance = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        instance.surf = surf
        instance.area = surf.get_rect()
        return instance

    def get_area_relative_top(
        area: pygame.Rect, pos_topleft: pygame.Vector2
    ) -> pygame.Rect:
        relative_area = area.copy()
        relative_area.topleft = pos_topleft.copy()
        return relative_area
