import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefabs_creator import create_enemy_square


def system_enemy_spawner(world: esper.World, delta_time: float):
    c_es: CEnemySpawner
    for _, (c_es,) in world.get_components(CEnemySpawner):
        c_es.current_time += delta_time
        for event in c_es.spawn_events:
            if not event["triggered"] and c_es.current_time >= event["time"]:
                enemy_type = event["enemy_type"]
                if enemy_type in c_es.enemies_cfg:
                    enemy_data = c_es.enemies_cfg[enemy_type]
                    create_enemy_square(world, enemy_data, event["position"])
                event["triggered"] = True
