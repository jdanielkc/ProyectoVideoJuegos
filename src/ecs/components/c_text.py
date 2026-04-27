import pygame


class CText:
    def __init__(
        self,
        text: str,
        font_path: str,
        font_size: int,
        color: pygame.Color,
        visible: bool = True,
    ) -> None:
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.visible = visible
        self.rendered_text = None
        self.rendered_visible = None
