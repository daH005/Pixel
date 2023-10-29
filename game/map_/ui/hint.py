from __future__ import annotations

from game.assets.images import HINT_IMAGES
from game.assets.fonts import FontSize
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.map_.map_ import Map
from game.map_.camera import Camera
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.contrib.windows import AbstractTextWindow
from game.contrib.screen import screen, SCREEN_W

__all__ = (
    'Hint',
)


@Map.add_object_type
class Hint(AbstractInteractingWithPlayerMapObject):
    Z_INDEX: int = 10
    size: SizeTupleType = HINT_IMAGES[0].get_size()
    ANIM_DELAY: float = 0.1
    TEXT_SHOWING_DELAY: float = 0.025
    TEXT_SHOWING_STEP: int = 1

    class TextWindow(AbstractTextWindow):
        FONT_SIZE: FontSize = FontSize.SMALL

        def __init__(self, text: str) -> None:
            self.text = text
            self.camera: Camera = Camera()
            super().__init__()

        def _draw(self) -> None:
            rect_to_draw = self.camera.apply(self.rect)
            if rect_to_draw.right > SCREEN_W:
                rect_to_draw.right = SCREEN_W
            screen.blit(self.image, rect_to_draw)

    def __init__(self, x: int, y: int, text: str) -> None:
        super().__init__(x, y)
        self.text = text.replace('\\n', '\n')
        self.anim_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(HINT_IMAGES),
            transition_delay_as_seconds=self.ANIM_DELAY,
        )

        self.windows: list[Hint.TextWindow] = self._build_windows()
        self.window_showing_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self.windows),
            transition_delay_as_seconds=self.TEXT_SHOWING_DELAY,
        )
        self.window_showing_enabled: bool = False

    def _build_windows(self) -> list[Hint.TextWindow]:
        windows: list[Hint.TextWindow] = []
        cur_text: str = ''
        for i in range(0, len(self.text), self.TEXT_SHOWING_STEP):
            cur_text += self.text[i:i+self.TEXT_SHOWING_STEP]
            windows.append(self.TextWindow(cur_text))
            windows[-1].rect.bottomleft = self.rect.topright
        return windows

    def update(self) -> None:
        self.window_showing_enabled = False
        super().update()

    def _update_image(self) -> None:
        self.image = HINT_IMAGES[self.anim_frames_counter.current_index]
        self.anim_frames_counter.next()

    def _draw(self) -> None:
        super()._draw()
        if self.window_showing_enabled:
            self.windows[self.window_showing_frames_counter.current_index].update()

    def _handle_collision_with_player(self) -> None:
        self.window_showing_enabled = True
        if not self.window_showing_frames_counter.is_last_frame:
            self.window_showing_frames_counter.next()
