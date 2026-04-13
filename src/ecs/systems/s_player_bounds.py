import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_bounds(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    screen_rect = screen.get_rect()

    for _, (c_t, c_s, _) in components:
        player_rect = c_s.surf.get_rect(topleft=c_t.pos)
        player_rect.clamp_ip(screen_rect)
        c_t.pos.x = player_rect.x
        c_t.pos.y = player_rect.y
