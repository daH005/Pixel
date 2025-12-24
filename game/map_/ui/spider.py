from pygame import Rect
from pygame.draw import rect as draw_rect

from engine.common.counters import FramesCounter
from engine.common.float_rect import FloatRect
from engine.common.colors import Color
from engine.map_.map_ import Map
from game.assets.images import SpiderImages
from game.map_.abstract_ui import AbstractMovingAndInteractingWithPlayerMapObject

__all__ = (
    'Spider',
)


@Map.add_object_type
class Spider(AbstractMovingAndInteractingWithPlayerMapObject):

    _IMAGES = SpiderImages
    _ANIMATION_DELAY: float = 0.075

    _SPEED: float = 1.75
    _SPIDERWEB_W: int = 2

    def __init__(self, map_: Map,
                 x: int, y: int,
                 end_y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(self._IMAGES.GO[0].get_rect(x=x, y=y)),
        )
        self._end_y = end_y

        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES.GO),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

        self._start_y: int = y
        self._y_vel: float = 0
        self._reaction_rect: Rect = Rect(self._rect.x, self._start_y, self._rect.w, self._end_y - self._start_y)

    def _move(self) -> None:
        self._y_vel = 0
        if self._reaction_rect.colliderect(self._map.player.get_rect()):
            if self._rect.bottom <= self._map.player._rect.y:
                self._y_vel = self._SPEED
        elif self._rect.y > self._start_y:
            self._y_vel = -self._SPEED
        self._rect.float_y += self._y_vel

    def _on_collision_with_player(self) -> None:
        self._map.player.hit()

    def _update_image(self) -> None:
        if self._y_vel:
            self._image = self._IMAGES.GO[self._go_frames_counter.current_index]
            self._go_frames_counter.next()
        else:
            self._image = self._IMAGES.STAND

    def _draw(self) -> None:
        self._draw_spiderweb()
        super()._draw()

    def _draw_spiderweb(self) -> None:
        draw_rect(self._screen, Color.WHITE, self._map.camera.apply_rect(self._make_spiderweb_rect()))

    def _make_spiderweb_rect(self) -> Rect:
        return Rect(
            self._rect.x + self._rect.w // 2 - self._SPIDERWEB_W // 2,
            self._start_y,
            self._SPIDERWEB_W,
            self._rect.y - self._start_y + self._rect.h // 2
        )
