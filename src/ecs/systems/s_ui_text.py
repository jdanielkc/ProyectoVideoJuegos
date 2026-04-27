import esper
import pygame

from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_player_special import CPlayerSpecial
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_ui_heart import CUiHeart
from src.ecs.components.c_ui_text import CUiText


def system_ui_text(world: esper.World, screen_width: int):
    paused = False
    cooldown_remaining = 0.0
    lives = 0
    game_over = False
    level_success = False

    game_state_components = world.get_components(CGameState)
    if len(game_state_components) > 0:
        _, (c_game_state,) = game_state_components[0]
        paused = c_game_state.paused
        lives = c_game_state.lives
        game_over = c_game_state.game_over
        level_success = c_game_state.level_success

    special_components = world.get_components(CPlayerSpecial)
    if len(special_components) > 0:
        _, (c_special,) = special_components[0]
        cooldown_remaining = c_special.cooldown_remaining

    for _, (c_text, c_ui_text, c_t, c_s) in world.get_components(
        CText,
        CUiText,
        CTransform,
        CSurface,
    ):
        if c_ui_text.role == "pause":
            c_text.visible = paused and not game_over and not level_success
            c_t.pos.x = (screen_width - c_s.area.w) / 2
        elif c_ui_text.role == "special_cooldown":
            if cooldown_remaining > 0:
                secs = int(cooldown_remaining) + 1
                c_text.text = f"E: {secs}S"
            else:
                c_text.text = "E: LISTO"
        elif c_ui_text.role == "game_over":
            c_text.visible = game_over
            c_t.pos.x = (screen_width - c_s.area.w) / 2
        elif c_ui_text.role == "level_success":
            c_text.visible = level_success
            c_t.pos.x = (screen_width - c_s.area.w) / 2
        elif c_ui_text.role == "restart_help":
            c_text.visible = game_over or level_success
            c_t.pos.x = (screen_width - c_s.area.w) / 2

        if c_ui_text.align == "right":
            c_t.pos.x = screen_width - c_s.area.w - 10

    # Mostrar / ocultar corazones según vidas restantes
    for _, (c_heart, c_s) in world.get_components(CUiHeart, CSurface):
        if c_heart.index < lives:
            c_s.area = c_heart.original_area.copy()
        else:
            c_s.area = pygame.Rect(0, 0, 0, 0)

