import esper

from src.ecs.components.c_move_sound import CMoveSound
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_player_movement_sound(world: esper.World, delta_time: float):
    for _, (c_velocity, c_move_sound) in world.get_components(CVelocity, CMoveSound):
        if c_move_sound.cooldown > 0:
            c_move_sound.cooldown -= delta_time

        if c_velocity.vel.magnitude_squared() <= 0:
            continue

        if c_move_sound.cooldown <= 0:
            ServiceLocator.sounds_service.play(c_move_sound.sound)
            c_move_sound.cooldown = c_move_sound.interval
