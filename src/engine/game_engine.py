import asyncio
import json
import sys

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_game_state import CGameState
from src.create.prefabs_creator import (
    create_bullet_square,
    create_heart,
    create_input_player,
    create_player_square,
    create_special_bullet_square,
    create_text,
)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_move_sound import CMoveSound
from src.ecs.components.c_player_special import CPlayerSpecial
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
from src.ecs.systems.s_game_state import system_game_state
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_movement_sound import system_player_movement_sound
from src.ecs.systems.s_player_bounds import system_player_bounds
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_special_cooldown import system_special_cooldown
from src.ecs.systems.s_text import system_text
from src.ecs.systems.s_ui_text import system_ui_text
from src.engine.service_locator import ServiceLocator


class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self._window_cfg = self._load_json("assets/cfg/window.json")
        self._enemies_cfg = self._load_json("assets/cfg/enemies.json")
        self._level_cfg = self._load_json("assets/cfg/level_01.json")
        self._player_cfg = self._load_json("assets/cfg/player.json")
        self._bullet_cfg = self._load_json("assets/cfg/bullet.json")
        self._explosion_cfg = self._load_json("assets/cfg/explosion.json")
        self._interface_cfg = self._load_json("assets/cfg/interface.json")
        self._special_cfg = self._load_json("assets/cfg/special.json")

        size = self._window_cfg["size"]
        self.screen = pygame.display.set_mode(
            (size["w"], size["h"]),
            self._get_display_flags(),
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

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(
            self.ecs_world, self._player_cfg, self._level_cfg["player_spawn"]
        )
        self.ecs_world.add_component(
            self._player_entity,
            CMoveSound(self._player_cfg["sound_move"]),
        )
        self.ecs_world.add_component(
            self._player_entity,
            CPlayerSpecial(self._special_cfg["cooldown"]),
        )
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity
        )
        self._game_state_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(self._game_state_entity, CGameState())
        spawner_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            spawner_entity, CEnemySpawner(self._level_cfg, self._enemies_cfg)
        )
        create_input_player(self.ecs_world)
        self._create_interface()

    def _calculate_time(self):
        self.clock.tick(self._framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        if not self._is_paused():
            system_enemy_spawner(self.ecs_world, self.delta_time)
            system_movement(self.ecs_world, self.delta_time)
            system_player_movement_sound(self.ecs_world, self.delta_time)
            system_player_state(self.ecs_world)
            system_hunter_state(self.ecs_world)
            system_screen_bounce(self.ecs_world, self.screen)
            system_player_bounds(self.ecs_world, self.screen)
            system_bullet_bounds(self.ecs_world, self.screen)
            system_collision_player_enemy(
                self.ecs_world,
                self._player_entity,
                self._level_cfg,
                self._explosion_cfg,
            )
            system_collision_bullet_enemy(self.ecs_world, self._explosion_cfg)
            system_animation(self.ecs_world, self.delta_time)
            system_special_cooldown(self.ecs_world, self.delta_time)
            system_explosion_cleanup(self.ecs_world)
            system_game_state(self.ecs_world)
            self.ecs_world._clear_dead_entities()

        system_ui_text(self.ecs_world, self.screen.get_width())
        system_text(self.ecs_world)

    def _draw(self):
        self.screen.fill(self._bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, action: CInputCommand):
        if action.name == "PLAYER_RESTART" and action.phase == CommandPhase.START:
            game_state = self.ecs_world.component_for_entity(
                self._game_state_entity, CGameState
            )
            if game_state.game_over or game_state.level_success:
                self._restart_game()
            return

        if action.name == "PLAYER_PAUSE" and action.phase == CommandPhase.START:
            self._toggle_pause()
            return

        if self._is_paused():
            return

        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            self._fire_bullet()
            return
        if action.name == "PLAYER_SPECIAL" and action.phase == CommandPhase.START:
            self._fire_special()
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

    def _fire_special(self):
        special = self.ecs_world.component_for_entity(
            self._player_entity, CPlayerSpecial
        )
        if special.cooldown_remaining > 0:
            return

        pl_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        pl_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        player_size = pygame.Vector2(pl_s.area.w, pl_s.area.h)
        directions = (
            pygame.Vector2(1, 1),
            pygame.Vector2(1, -1),
            pygame.Vector2(-1, 1),
            pygame.Vector2(-1, -1),
        )

        for direction in directions:
            create_special_bullet_square(
                self.ecs_world,
                self._special_cfg,
                pl_t.pos,
                player_size,
                direction,
            )

        special.cooldown_remaining = special.cooldown_duration
        ServiceLocator.sounds_service.play(self._special_cfg["sound"])

    def _create_interface(self):
        font_path = self._interface_cfg["font"]
        texts_cfg = self._interface_cfg["texts"]
        create_text(self.ecs_world, font_path, texts_cfg["title"])
        create_text(self.ecs_world, font_path, texts_cfg["move_help"])
        create_text(self.ecs_world, font_path, texts_cfg["fire_help"])
        create_text(self.ecs_world, font_path, texts_cfg["special_help"], align="right")
        create_text(self.ecs_world, font_path, texts_cfg["pause_help"], align="right")
        create_text(
            self.ecs_world,
            font_path,
            texts_cfg["pause"],
            ui_role="pause",
            visible=False,
        )
        create_text(
            self.ecs_world,
            font_path,
            texts_cfg["special_cooldown"],
            ui_role="special_cooldown",
            align="right",
        )
        if "game_over" in texts_cfg:
            create_text(
                self.ecs_world,
                font_path,
                texts_cfg["game_over"],
                ui_role="game_over",
                visible=False,
            )
        if "level_success" in texts_cfg:
            create_text(
                self.ecs_world,
                font_path,
                texts_cfg["level_success"],
                ui_role="level_success",
                visible=False,
            )
        if "restart_help" in texts_cfg:
            create_text(
                self.ecs_world,
                font_path,
                texts_cfg["restart_help"],
                ui_role="restart_help",
                visible=False,
            )

        # Corazones de vida (HUD superior, centrado)
        game_state = self.ecs_world.component_for_entity(
            self._game_state_entity, CGameState
        )
        heart_size = 12
        spacing = 4
        total_width = game_state.max_lives * heart_size + (game_state.max_lives - 1) * spacing
        screen_w = self.screen.get_width()
        start_x = (screen_w - total_width) // 2
        y = 8
        for i in range(game_state.max_lives):
            x = start_x + i * (heart_size + spacing)
            create_heart(self.ecs_world, i, pygame.Vector2(x, y))

    def _is_paused(self) -> bool:
        game_state = self.ecs_world.component_for_entity(
            self._game_state_entity,
            CGameState,
        )
        return game_state.paused or game_state.game_over or game_state.level_success

    def _toggle_pause(self):
        game_state = self.ecs_world.component_for_entity(
            self._game_state_entity,
            CGameState,
        )
        game_state.paused = not game_state.paused
        if game_state.paused:
            self._player_c_v.vel.x = 0
            self._player_c_v.vel.y = 0

    def _restart_game(self):
        self.ecs_world.clear_database()
        self._create()

    def _get_display_flags(self) -> int:
        return 0
