from typing import List


class CAnimation:
    def __init__(self, animations: dict, looping: bool = True) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = []
        for anim in animations["list"]:
            anim_data = AnimationData(
                name=anim["name"],
                start=anim["start"],
                end=anim["end"],
                framerate=anim["framerate"],
            )
            self.animations_list.append(anim_data)
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start
        self.looping = looping
        self.finished = False


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate
