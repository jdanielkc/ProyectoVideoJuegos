import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefabs_creator import create_enemy_square, create_hunter_enemy


def system_enemy_spawner(world: esper.World, delta_time: float):
    c_es: CEnemySpawner
    for _, (c_es,) in world.get_components(CEnemySpawner):
        c_es.current_time += delta_time
        for event in c_es.spawn_events:
            if not event["triggered"] and c_es.current_time >= event["time"]:
                _spawn_enemy(world, event, c_es.enemies_cfg)
                event["triggered"] = True


def _spawn_enemy(world: esper.World, event: dict, enemies_cfg: dict):
    enemy_type = event["enemy_type"]
    if enemy_type not in enemies_cfg:
        return
    enemy_data = enemies_cfg[enemy_type]
    if "animations" in enemy_data:
        create_hunter_enemy(world, enemy_data, event["position"])
    else:
        create_enemy_square(world, enemy_data, event["position"])
