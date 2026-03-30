import json

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self._window_cfg = self._load_json("assets/cfg/window.json")
        self._enemies_cfg = self._load_json("assets/cfg/enemies.json")
        self._level_cfg = self._load_json("assets/cfg/level_01.json")

        size = self._window_cfg["size"]
        self.screen = pygame.display.set_mode(
            (size["w"], size["h"]), pygame.SCALED
        )
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
        spawner_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            spawner_entity,
            CEnemySpawner(self._level_cfg, self._enemies_cfg)
        )

    def _calculate_time(self):
        self.clock.tick(self._framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(self._bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
