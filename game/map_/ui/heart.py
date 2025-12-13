from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import HEART_IMAGES
from game.assets.sounds import heart_sound

__all__ = (
    'Heart',
)


@Map.add_object_type
class Heart(AbstractInteractingWithPlayerMapObject):

    _IMAGES = HEART_IMAGES
    _ANIMATION_DELAY: float = 1

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._IMAGES[0].get_rect(x=x, y=y),
        )
        self.frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

    def _update_image(self) -> None:
        self._image = self._IMAGES[self.frames_counter.current_index]
        self.frames_counter.next()

    def _handle_collision_with_player(self) -> None:
        if self._map.player.hp < self._map.player.max_hp:
            self._to_delete = True
            self._map.player.replenish_hp()
            heart_sound.play()
