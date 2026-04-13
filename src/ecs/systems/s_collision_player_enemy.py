import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_player_enemy(
    world: esper.World, player_entity: int, level_cfg: dict
):
    components = world.get_components(CTransform, CSurface, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = pl_s.surf.get_rect(topleft=pl_t.pos)

    for entity, (c_t, c_s, c_e) in components:
        enemy_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if pl_rect.colliderect(enemy_rect):
            world.delete_entity(entity)
            print("Player collided with an enemy!")
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - (pl_s.surf.get_width() / 2)
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - (pl_s.surf.get_height() / 2)
