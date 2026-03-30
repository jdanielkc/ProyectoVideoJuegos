class CEnemySpawner:
    def __init__(self, level_data: dict, enemies_cfg: dict) -> None:
        self.enemies_cfg = enemies_cfg
        self.current_time = 0.0
        self.spawn_events = []
        for event in level_data.get("enemy_spawn_events", []):
            self.spawn_events.append(
                {
                    "time": event["time"],
                    "enemy_type": event["enemy_type"],
                    "position": event["position"],
                    "triggered": False,
                }
            )
