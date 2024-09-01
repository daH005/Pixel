from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from game.assets.images import HINT_IMAGES
from game.assets.fonts import PixelFonts
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.common.windows.building import TextWindowPartsSurfacesBuilder
from game.common.windows.windows import TextWindow

__all__ = (
    'Hint',
)


@Map.add_object_type
class Hint(AbstractInteractingWithPlayerMapObject):
    _Z_INDEX: int = 10

    def __init__(self, map_: Map,
                 x: int, y: int,
                 text: str,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=HINT_IMAGES[0].get_rect(x=x, y=y),
            z_index=self._Z_INDEX,
        )

        self._x = x
        self._y = y
        self._text = text

        self._anim_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(HINT_IMAGES),
            transition_delay_as_seconds=0.09,
        )

        self._text_showing_step: int = 1
        self._window_showing_enabled: bool = False
        self._init_windows()
        self._window_showing_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._windows),
            transition_delay_as_seconds=0.025,
        )

    def _init_windows(self) -> None:
        self._windows: list[TextWindow] = []
        current_text: str = ''
        for i in range(0, len(self._text), self._text_showing_step):
            current_text += self._text[i:i+self._text_showing_step]

            window: _HintTextWindow = _HintTextWindow(
                map_=self._map,
                x=self._x + self._rect.w,
                y=self._y,
                text=current_text,
            )
            self._windows.append(window)

    def update(self) -> None:
        self._window_showing_enabled = False
        super().update()

    def _update_image(self) -> None:
        self._image = HINT_IMAGES[self._anim_frames_counter.current_index]
        self._anim_frames_counter.next()

    def _draw(self) -> None:
        super()._draw()
        if self._window_showing_enabled:
            self._windows[self._window_showing_frames_counter.current_index].update()

    def _handle_collision_with_player(self) -> None:
        self._window_showing_enabled = True
        if not self._window_showing_frames_counter.is_last_frame:
            self._window_showing_frames_counter.next()


class _HintTextWindow(TextWindow):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 text: str) -> None:
        super().__init__(
            builder=TextWindowPartsSurfacesBuilder(
                text=text,
                font=PixelFonts.SMALL,
            ),
            x=x, y=y,
        )
        self._map = map_

    def _draw(self) -> None:
        rect_to_draw = self._map.camera.apply(self._rect)
        if rect_to_draw.right > self._screen.get_width():
            rect_to_draw.right = self._screen.get_width()
        self._screen.blit(self._image, rect_to_draw)
