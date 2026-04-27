class CMoveSound:
    def __init__(self, sound: str, interval: float = 0.35) -> None:
        self.sound = sound
        self.interval = interval
        self.cooldown = 0.0
