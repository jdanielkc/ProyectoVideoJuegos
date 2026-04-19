from enum import Enum

import pygame


class CHunterState:
    def __init__(
        self,
        origin: pygame.Vector2,
        velocity_chase: float,
        velocity_return: float,
        distance_start_chase: float,
        distance_start_return: float,
    ) -> None:
        self.origin = origin.copy()
        self.velocity_chase = velocity_chase
        self.velocity_return = velocity_return
        self.distance_start_chase = distance_start_chase
        self.distance_start_return = distance_start_return
        self.state = HunterState.IDLE


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2
