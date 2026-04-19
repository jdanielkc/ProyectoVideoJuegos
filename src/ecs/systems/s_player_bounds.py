import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_bounds(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    screen_rect = screen.get_rect()

    for _, (c_t, c_s, _) in components:
        player_rect = CSurface.get_area_relative_top(c_s.area, c_t.pos)
        if player_rect.left < screen_rect.left:
            c_t.pos.x = screen_rect.left
        elif player_rect.right > screen_rect.right:
            c_t.pos.x = screen_rect.right - player_rect.width

        if player_rect.top < screen_rect.top:
            c_t.pos.y = screen_rect.top
        elif player_rect.bottom > screen_rect.bottom:
            c_t.pos.y = screen_rect.bottom - player_rect.height
