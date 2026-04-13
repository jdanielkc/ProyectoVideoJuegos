import math
import random

import esper
import pygame
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def crear_cuadrado_prefab(
    world: esper.World,
    size: pygame.Vector2,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    col: pygame.Color,
) -> int:
    cuad_entity = world.create_entity()
    world.add_component(
        cuad_entity,
        CSurface(size=size, color=col),
    )
    world.add_component(cuad_entity, CTransform(pos=pos))
    world.add_component(cuad_entity, CVelocity(vel=vel))
    return cuad_entity


def create_player_square(
    world: esper.World,
    player_cfg: dict,
    player_spawn: dict,
) -> int:
    size = pygame.Vector2(player_cfg["size"]["x"], player_cfg["size"]["y"])
    col = pygame.Color(
        player_cfg["color"]["r"],
        player_cfg["color"]["g"],
        player_cfg["color"]["b"],
    )
    pos = pygame.Vector2(
        player_spawn["position"]["x"] - (size.x / 2),
        player_spawn["position"]["y"] - (size.y / 2),
    )
    vel = pygame.Vector2(0, 0)
    player_entity = crear_cuadrado_prefab(world, size=size, pos=pos, vel=vel, col=col)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_enemy_square(
    world: esper.World,
    enemy_data: dict,
    position: dict,
):
    size = pygame.Vector2(enemy_data["size"]["x"], enemy_data["size"]["y"])
    col = pygame.Color(
        enemy_data["color"]["r"],
        enemy_data["color"]["g"],
        enemy_data["color"]["b"],
    )
    pos = pygame.Vector2(position["x"], position["y"])
    vel_min = enemy_data["velocity_min"]
    vel_max = enemy_data["velocity_max"]
    speed = random.uniform(vel_min, vel_max)
    angle = random.uniform(0, 2 * math.pi)
    vel = pygame.Vector2(
        math.cos(angle) * speed,
        math.sin(angle) * speed,
    )
    enemy_entity = crear_cuadrado_prefab(world, size=size, pos=pos, vel=vel, col=col)
    world.add_component(enemy_entity, CTagEnemy())


def create_bullet_square(
    world: esper.World,
    bullet_cfg: dict,
    player_pos: pygame.Vector2,
    player_size: pygame.Vector2,
    mouse_pos: tuple,
):
    size = pygame.Vector2(bullet_cfg["size"]["x"], bullet_cfg["size"]["y"])
    col = pygame.Color(
        bullet_cfg["color"]["r"],
        bullet_cfg["color"]["g"],
        bullet_cfg["color"]["b"],
    )
    center_x = player_pos.x + player_size.x / 2
    center_y = player_pos.y + player_size.y / 2
    pos = pygame.Vector2(center_x - size.x / 2, center_y - size.y / 2)

    direction = pygame.Vector2(mouse_pos[0] - center_x, mouse_pos[1] - center_y)
    if direction.length() == 0:
        direction = pygame.Vector2(1, 0)
    direction = direction.normalize()
    vel = direction * bullet_cfg["velocity"]

    bullet_entity = crear_cuadrado_prefab(world, size=size, pos=pos, vel=vel, col=col)
    world.add_component(bullet_entity, CTagBullet())


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    input_right = world.create_entity()
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    input_up = world.create_entity()
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    input_down = world.create_entity()
    world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    input_left_a = world.create_entity()
    world.add_component(input_left_a, CInputCommand("PLAYER_LEFT", pygame.K_a))
    input_right_d = world.create_entity()
    world.add_component(input_right_d, CInputCommand("PLAYER_RIGHT", pygame.K_d))
    input_up_w = world.create_entity()
    world.add_component(input_up_w, CInputCommand("PLAYER_UP", pygame.K_w))
    input_down_s = world.create_entity()
    world.add_component(input_down_s, CInputCommand("PLAYER_DOWN", pygame.K_s))