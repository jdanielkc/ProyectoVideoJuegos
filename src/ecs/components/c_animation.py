from typing import List


class CAnimation:
    def __init__(self, animations: dict) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = []
        for anim in animations["list"]:
            anim_data = AnimationData(
                name=anim["name"],
                start=anim["start"],
                end=anim["end"],
                frame_rate=anim["frame_rate"],
            )
            self.animations_list.append(anim_data)
        self.current_animation = 0
        self.current_animation_time = self.animations_list[
            self.current_animation
        ].frame_rate


class AnimationData:
    def __init__(self, name: str, start: int, end: int, frame_rate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.frame_rate = 1.0 / frame_rate
