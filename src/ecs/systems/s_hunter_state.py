import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_hunter_state(world: esper.World):
    player_components = world.get_components(CTransform, CSurface, CTagPlayer)
    if len(player_components) == 0:
        return
    _, (pl_t, pl_s, _) = player_components[0]
    player_center = pygame.Vector2(
        pl_t.pos.x + pl_s.area.w / 2,
        pl_t.pos.y + pl_s.area.h / 2,
    )

    hunters = world.get_components(
        CTransform, CVelocity, CSurface, CAnimation, CHunterState
    )
    for entity, (c_t, c_v, c_s, c_a, c_h) in hunters:
        hunter_center = pygame.Vector2(
            c_t.pos.x + c_s.area.w / 2,
            c_t.pos.y + c_s.area.h / 2,
        )

        if c_h.state == HunterState.IDLE:
            _do_idle(c_v, c_a, c_h, hunter_center, player_center)
        elif c_h.state == HunterState.CHASE:
            _do_chase(c_v, c_a, c_h, hunter_center, player_center)
        elif c_h.state == HunterState.RETURN:
            _do_return(c_t, c_v, c_a, c_s, c_h, hunter_center)


def _do_idle(
    c_v: CVelocity,
    c_a: CAnimation,
    c_h: CHunterState,
    hunter_center: pygame.Vector2,
    player_center: pygame.Vector2,
):
    c_v.vel.x = 0
    c_v.vel.y = 0
    _set_animation(c_a, 1)
    dist = hunter_center.distance_to(player_center)
    if dist <= c_h.distance_start_chase:
        c_h.state = HunterState.CHASE


def _do_chase(
    c_v: CVelocity,
    c_a: CAnimation,
    c_h: CHunterState,
    hunter_center: pygame.Vector2,
    player_center: pygame.Vector2,
):
    _set_animation(c_a, 0)
    direction = player_center - hunter_center
    if direction.length() > 0:
        direction = direction.normalize()
    c_v.vel = direction * c_h.velocity_chase

    dist_from_origin = hunter_center.distance_to(c_h.origin)
    if dist_from_origin >= c_h.distance_start_return:
        c_h.state = HunterState.RETURN


def _do_return(
    c_t: CTransform,
    c_v: CVelocity,
    c_a: CAnimation,
    c_s: CSurface,
    c_h: CHunterState,
    hunter_center: pygame.Vector2,
):
    _set_animation(c_a, 0)
    direction = c_h.origin - hunter_center
    dist = direction.length()
    if dist < 2:
        c_t.pos.x = c_h.origin.x - c_s.area.w / 2
        c_t.pos.y = c_h.origin.y - c_s.area.h / 2
        c_v.vel.x = 0
        c_v.vel.y = 0
        c_h.state = HunterState.IDLE
        return
    direction = direction.normalize()
    c_v.vel = direction * c_h.velocity_return


def _set_animation(animation: CAnimation, animation_index: int):
    if animation.current_animation == animation_index:
        return
    animation.current_animation = animation_index
    animation.current_animation_time = 0
    animation.current_frame = animation.animations_list[
        animation.current_animation
    ].start
