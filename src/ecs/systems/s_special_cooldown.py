import esper

from src.ecs.components.c_player_special import CPlayerSpecial


def system_special_cooldown(world: esper.World, delta_time: float):
    for _, (c_special,) in world.get_components(CPlayerSpecial):
        c_special.cooldown_remaining = max(
            0.0,
            c_special.cooldown_remaining - delta_time,
        )
