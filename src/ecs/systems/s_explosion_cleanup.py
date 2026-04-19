import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_cleanup(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for entity, (c_a, _) in components:
        if c_a.finished:
            world.delete_entity(entity)
