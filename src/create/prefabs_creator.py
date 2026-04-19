import math
import random

import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
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
    player_sprite = pygame.image.load(player_cfg["image"]).convert_alpha()
    frame_width = player_sprite.get_width() / player_cfg["animations"]["number_frames"]
    pos = pygame.Vector2(
        player_spawn["position"]["x"] - (frame_width / 2),
        player_spawn["position"]["y"] - (player_sprite.get_height() / 2),
    )
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos=pos, vel=vel, surface=player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_cfg["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_enemy_square(
    world: esper.World,
    enemy_data: dict,
    position: dict,
):
    enemy_surface = pygame.image.load(enemy_data["image"]).convert_alpha()
    pos = pygame.Vector2(position["x"], position["y"])
    vel_min = enemy_data["velocity_min"]
    vel_max = enemy_data["velocity_max"]
    speed = random.uniform(vel_min, vel_max)
    angle = random.uniform(0, 2 * math.pi)
    vel = pygame.Vector2(
        math.cos(angle) * speed,
        math.sin(angle) * speed,
    )
    enemy_entity = create_sprite(world, pos=pos, vel=vel, surface=enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())


def create_sprite(
    world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos=pos))
    world.add_component(sprite_entity, CVelocity(vel=vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_bullet_square(
    world: esper.World,
    bullet_cfg: dict,
    player_pos: pygame.Vector2,
    player_size: pygame.Vector2,
    mouse_pos: tuple,
):
    bullet_surface = pygame.image.load(bullet_cfg["image"]).convert_alpha()
    center_x = player_pos.x + player_size.x / 2
    center_y = player_pos.y + player_size.y / 2
    pos = pygame.Vector2(
        center_x - bullet_surface.get_width() / 2,
        center_y - bullet_surface.get_height() / 2,
    )

    direction = pygame.Vector2(mouse_pos[0] - center_x, mouse_pos[1] - center_y)
    if direction.length() == 0:
        direction = pygame.Vector2(1, 0)
    direction = direction.normalize()
    vel = direction * bullet_cfg["velocity"]

    bullet_entity = create_sprite(world, pos=pos, vel=vel, surface=bullet_surface)
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
