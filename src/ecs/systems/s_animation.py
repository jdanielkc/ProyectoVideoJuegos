import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float):
    components = world.get_components(CSurface, CAnimation)
    for entity, (surface, animation) in components:
        animation.current_animation_time -= delta_time
        if animation.current_animation_time <= 0:
            animation.current_animation_time = animation.animations_list[
                animation.current_animation
            ].frame_rate
            animation.current_frame += 1
            if (
                animation.current_frame
                > animation.animations_list[animation.current_animation].end
            ):
                animation.current_frame = animation.animations_list[
                    animation.current_animation
                ].start
            rect = surface.surf.get_rect()
            surface.area.w = rect.w / animation.number_frames
            surface.area.x = surface.area.w * animation.current_frame
