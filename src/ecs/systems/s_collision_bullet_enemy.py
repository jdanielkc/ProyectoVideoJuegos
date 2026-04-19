import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_bullet_enemy(world: esper.World):
    bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for b_entity, (b_t, b_s, _) in bullets:
        bullet_rect = CSurface.get_area_relative_top(b_s.area, b_t.pos)
        for e_entity, (e_t, e_s, _) in enemies:
            enemy_rect = CSurface.get_area_relative_top(e_s.area, e_t.pos)
            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(b_entity)
                world.delete_entity(e_entity)
                break
