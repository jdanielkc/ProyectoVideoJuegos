class CPlayerSpecial:
    def __init__(self, cooldown_duration: float) -> None:
        self.cooldown_duration = cooldown_duration
        self.cooldown_remaining = 0.0
