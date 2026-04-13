from typing import Callable

import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(
    world: esper.World,
    event: pygame.event.Event,
    do_action: Callable[[CInputCommand], None],
):
    componets = world.get_components(CInputCommand)
    for _, (c_input_command,) in componets:
        if event.type == pygame.KEYDOWN and c_input_command.key == event.key:
            c_input_command.phase = CommandPhase.START
            do_action(c_input_command)
        elif event.type == pygame.KEYUP and c_input_command.key == event.key:
            c_input_command.phase = CommandPhase.END
            do_action(c_input_command)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        fire_cmd = CInputCommand("PLAYER_FIRE", 0)
        fire_cmd.phase = CommandPhase.START
        do_action(fire_cmd)
