import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.engine.service_locator import ServiceLocator


def system_text(world: esper.World):
    for _, (c_s, c_text) in world.get_components(CSurface, CText):
        if not c_text.visible:
            if c_text.rendered_visible is not False:
                c_s.surf = pygame.Surface((1, 1), pygame.SRCALPHA)
                c_s.area = c_s.surf.get_rect()
                c_text.rendered_visible = False
            continue

        if (
            c_text.rendered_text == c_text.text
            and c_text.rendered_visible is True
        ):
            continue

        font = ServiceLocator.fonts_service.get(c_text.font_path, c_text.font_size)
        c_s.surf = font.render(c_text.text, False, c_text.color)
        c_s.area = c_s.surf.get_rect()
        c_text.rendered_text = c_text.text
        c_text.rendered_visible = True
