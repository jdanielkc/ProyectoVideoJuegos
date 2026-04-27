import esper
import pygame

from src.create.prefabs_creator import create_explosion
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_player_enemy(
    world: esper.World, player_entity: int, level_cfg: dict, explosion_cfg: dict
):
    components = world.get_components(CTransform, CSurface, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative_top(pl_s.area, pl_t.pos)

    for entity, (c_t, c_s, c_e) in components:
        enemy_rect = CSurface.get_area_relative_top(c_s.area, c_t.pos)
        if pl_rect.colliderect(enemy_rect):
            explosion_pos = pygame.Vector2(
                enemy_rect.centerx, enemy_rect.centery
            )
            world.delete_entity(entity)
            create_explosion(world, explosion_cfg, explosion_pos)
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - (
                pl_s.area.w / 2
            )
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - (
                pl_s.area.h / 2
            )

            # Restar una vida y comprobar game over
            game_state_components = world.get_components(CGameState)
            if len(game_state_components) > 0:
                _, (c_game_state,) = game_state_components[0]
                if not c_game_state.game_over and not c_game_state.level_success:
                    c_game_state.lives -= 1
                    if c_game_state.lives <= 0:
                        c_game_state.lives = 0
                        c_game_state.game_over = True
                        # Detener al jugador
                        try:
                            pl_v = world.component_for_entity(
                                player_entity, CVelocity
                            )
                            pl_v.vel.x = 0
                            pl_v.vel.y = 0
                        except KeyError:
                            pass
            return

