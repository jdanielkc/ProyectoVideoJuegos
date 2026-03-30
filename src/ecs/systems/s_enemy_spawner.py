import math
import random

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefabs_creator import crear_cuadrado_prefab


def system_enemy_spawner(world: esper.World, delta_time: float):
    c_es: CEnemySpawner
    for _, (c_es,) in world.get_components(CEnemySpawner):
        c_es.current_time += delta_time
        for event in c_es.spawn_events:
            if not event["triggered"] and c_es.current_time >= event["time"]:
                enemy_type = event["enemy_type"]
                if enemy_type in c_es.enemies_cfg:
                    enemy_data = c_es.enemies_cfg[enemy_type]
                    size = pygame.Vector2(
                        enemy_data["size"]["x"],
                        enemy_data["size"]["y"]
                    )
                    col = pygame.Color(
                        enemy_data["color"]["r"],
                        enemy_data["color"]["g"],
                        enemy_data["color"]["b"]
                    )
                    pos = pygame.Vector2(
                        event["position"]["x"],
                        event["position"]["y"]
                    )
                    vel_min = enemy_data["velocity_min"]
                    vel_max = enemy_data["velocity_max"]
                    speed = random.uniform(vel_min, vel_max)
                    angle = random.uniform(0, 2 * math.pi)
                    vel = pygame.Vector2(
                        math.cos(angle) * speed,
                        math.sin(angle) * speed
                    )
                    crear_cuadrado_prefab(world, size=size, pos=pos, vel=vel, col=col)
                event["triggered"] = True
