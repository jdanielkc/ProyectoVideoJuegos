import json

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefabs_creator import (
    create_bullet_square,
    create_input_player,
    create_player_square,
)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_bounds import system_bullet_bounds
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_cleanup import system_explosion_cleanup
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bounds import system_player_bounds
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self._window_cfg = self._load_json("assets/cfg/window.json")
        self._enemies_cfg = self._load_json("assets/cfg/enemies.json")
        self._level_cfg = self._load_json("assets/cfg/level_01.json")
        self._player_cfg = self._load_json("assets/cfg/player.json")
        self._bullet_cfg = self._load_json("assets/cfg/bullet.json")
        self._explosion_cfg = self._load_json("assets/cfg/explosion.json")

        size = self._window_cfg["size"]
        self.screen = pygame.display.set_mode((size["w"], size["h"]), pygame.SCALED)
        pygame.display.set_caption(self._window_cfg["title"])

        bg = self._window_cfg["bg_color"]
        self._bg_color = pygame.Color(bg["r"], bg["g"], bg["b"])
        self._framerate = self._window_cfg["framerate"]

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.delta_time = 0

        self.ecs_world = esper.World()

    def _load_json(self, path: str) -> dict:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(
            self.ecs_world, self._player_cfg, self._level_cfg["player_spawn"]
        )
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity
        )
        spawner_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            spawner_entity, CEnemySpawner(self._level_cfg, self._enemies_cfg)
        )
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self._framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        system_screen_bounce(self.ecs_world, self.screen)
        system_player_bounds(self.ecs_world, self.screen)
        system_bullet_bounds(self.ecs_world, self.screen)
        system_collision_player_enemy(
            self.ecs_world, self._player_entity, self._level_cfg, self._explosion_cfg
        )
        system_collision_bullet_enemy(self.ecs_world, self._explosion_cfg)
        system_animation(self.ecs_world, self.delta_time)
        system_explosion_cleanup(self.ecs_world)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self._bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, action: CInputCommand):
        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            self._fire_bullet()
            return
        sign = 1 if action.phase == CommandPhase.START else -1
        speed = self._player_cfg["input_velocity"]
        move_map = {
            "PLAYER_LEFT": (-sign * speed, 0),
            "PLAYER_RIGHT": (sign * speed, 0),
            "PLAYER_UP": (0, -sign * speed),
            "PLAYER_DOWN": (0, sign * speed),
        }
        if action.name in move_map:
            dx, dy = move_map[action.name]
            self._player_c_v.vel.x += dx
            self._player_c_v.vel.y += dy

    def _fire_bullet(self):
        max_bullets = self._level_cfg["player_spawn"].get("max_bullets", 1)
        current_bullets = len(self.ecs_world.get_components(CTagBullet))
        if current_bullets >= max_bullets:
            return
        pl_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        pl_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        player_size = pygame.Vector2(pl_s.area.w, pl_s.area.h)
        mouse_pos = pygame.mouse.get_pos()
        create_bullet_square(
            self.ecs_world, self._bullet_cfg, pl_t.pos, player_size, mouse_pos
        )
