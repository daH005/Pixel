from game.assets.images import COIN_IMAGES
from game.assets.sounds import coin_sound
from game.assets.levels import LevelsManager
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType, XYTupleType
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.contrib.screen import SCREEN_RECT, screen
from game.contrib.rects import FloatRect
from game.map_.exceptions import MapObjectCannotBeCreated

__all__ = (
    'Coin',
)


@Map.add_object_type
class Coin(AbstractInteractingWithPlayerMapObject):
    Z_INDEX = 2
    size: SizeTupleType = COIN_IMAGES[0].get_size()
    ANIM_DELAY: float = 0.15

    FLYING_END_X_Y: XYTupleType = SCREEN_RECT.topright
    FLYING_SPEED: float = 15
    flying_rect: FloatRect

    def __init__(self, x: int, y: int, id_: int | None = None) -> None:
        if id_ in LevelsManager.current_level.uncreating_ids:
            raise MapObjectCannotBeCreated
        super().__init__(x, y)
        self.id = id_
        self.frames_counter: FramesCounter = FramesCounter(
            frames_count=len(COIN_IMAGES),
            transition_delay_as_seconds=self.ANIM_DELAY,
        )
        self.is_taken: bool = False

    def update(self) -> None:
        if self.is_taken:
            self._fly()
        super().update()

    def _update_image(self) -> None:
        self.image = COIN_IMAGES[self.frames_counter.current_index]
        self.frames_counter.next()

    def _fly(self) -> None:
        x_dis: float = abs(self.FLYING_END_X_Y[0] - self.flying_rect.float_x)
        y_dis: float = abs(self.FLYING_END_X_Y[1] - self.flying_rect.float_y)
        hypotenuse: float = (x_dis ** 2 + y_dis ** 2) ** 0.5
        if hypotenuse == 0:
            hypotenuse = 1
        self.flying_rect.float_x += self.FLYING_SPEED * (x_dis / hypotenuse)
        self.flying_rect.float_y -= self.FLYING_SPEED * (y_dis / hypotenuse)
        if self.flying_rect.x > self.FLYING_END_X_Y[0] and self.flying_rect.y < self.FLYING_END_X_Y[1]:
            self.to_delete = True
            self.map.visual_taken_coins_count += 1
            coin_sound.play()

    def _handle_collision_with_player(self) -> None:
        if not self.is_taken:
            self.take()

    def take(self) -> None:
        self.is_taken = True
        self.flying_rect = FloatRect(self.camera.apply(self.rect))
        self.map.taken_coins_count += 1
        if self.id is not None:
            self.map.uncreating_ids.append(self.id)

    def _draw(self) -> None:
        if not self.is_taken:
            super()._draw()
        else:
            screen.blit(self.image, self.flying_rect)
