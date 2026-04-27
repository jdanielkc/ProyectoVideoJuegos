import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_game_state(world: esper.World):
    game_state_components = world.get_components(CGameState)
    if len(game_state_components) == 0:
        return
    _, (c_game_state,) = game_state_components[0]

    if c_game_state.game_over or c_game_state.level_success:
        return

    # Verificar si todos los eventos de spawn ya ocurrieron
    all_spawned = True
    for _, (c_es,) in world.get_components(CEnemySpawner):
        for event in c_es.spawn_events:
            if not event["triggered"]:
                all_spawned = False
                break
        if not all_spawned:
            break

    enemies_remaining = len(world.get_components(CTagEnemy))

    if all_spawned and enemies_remaining == 0:
        c_game_state.level_success = True
