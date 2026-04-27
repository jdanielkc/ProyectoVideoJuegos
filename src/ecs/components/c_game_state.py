class CGameState:
    def __init__(self, lives: int = 3) -> None:
        self.paused = False
        self.lives = lives
        self.max_lives = lives
        self.game_over = False
        self.level_success = False
        self.total_spawn_events = 0
