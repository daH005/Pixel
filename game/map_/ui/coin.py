from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from engine.common.typing_ import XYTupleType
from engine.common.float_rect import FloatRect
from game.assets.images import COIN_IMAGES
from game.assets.sounds import coin_sound
from game.map_.abstract_ui import AbstractItemToDisposableCollect

__all__ = (
    'Coin',
)


@Map.add_object_type
class Coin(AbstractItemToDisposableCollect):

    _Z_INDEX_WHEN_IS_TAKEN: int = 999
    _IMAGES = COIN_IMAGES
    _ANIMATION_DELAY: float = 0.15

    _collected_count: int = 0
    _visual_collected_count: int = 0

    _flying_rect: FloatRect
    _FLYING_SPEED: float = 15

    def __init__(self, map_: Map,
                 x: int, y: int,
                 id_: int | None = None,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._IMAGES[0].get_rect(x=x, y=y),
            id_=id_,
        )

        self._frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

        self._is_taken: bool = False
        self._flying_end_xy: XYTupleType = self._screen.get_rect().topright
        self._z_index: int = self._Z_INDEX

    @classmethod
    def reset_class(cls) -> None:
        cls._collected_count = 0
        cls._visual_collected_count = 0

    @property
    def z_index(self) -> int:
        return self._z_index

    @classmethod
    @property
    def collected_count(cls) -> int:
        return cls._collected_count

    @classmethod
    @property
    def visual_collected_count(cls) -> int:
        return cls._visual_collected_count

    def update(self) -> None:
        if self._is_taken:
            self._fly()
        super().update()

    def _update_image(self) -> None:
        self._image = self._IMAGES[self._frames_counter.current_index]
        self._frames_counter.next()

    def _fly(self) -> None:
        x_dis: float = abs(self._flying_end_xy[0] - self._flying_rect.float_x)
        y_dis: float = abs(self._flying_end_xy[1] - self._flying_rect.float_y)
        hypotenuse: float = (x_dis ** 2 + y_dis ** 2) ** 0.5
        if hypotenuse == 0:
            hypotenuse = 1

        self._flying_rect.float_x += self._FLYING_SPEED * (x_dis / hypotenuse)
        self._flying_rect.float_y -= self._FLYING_SPEED * (y_dis / hypotenuse)
        if self._flying_rect.x > self._flying_end_xy[0] and self._flying_rect.y < self._flying_end_xy[1]:
            self._to_delete = True
            type(self)._visual_collected_count += 1
            coin_sound.play()

    def _handle_collision_with_player(self) -> None:
        if not self._is_taken:
            self.take()

    def take(self) -> None:
        super().take()
        self._z_index = self._Z_INDEX_WHEN_IS_TAKEN
        self._is_taken = True
        self._flying_rect = FloatRect(self._map.camera.apply_rect(self._rect))
        type(self)._collected_count += 1

    def _draw(self) -> None:
        if not self._is_taken:
            super()._draw()
        else:
            self._screen.blit(self._image, self._flying_rect)
