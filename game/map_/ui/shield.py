from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from game.assets.images import SHIELD_IMAGES
from game.assets.sounds import shield_sound
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject

__all__ = (
    'Shield',
)


@Map.add_object_type
class Shield(AbstractInteractingWithPlayerMapObject):

    _IMAGES = SHIELD_IMAGES
    _ANIMATION_DELAY: float = 0.1

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._IMAGES[0].get_rect(x=x, y=y),
        )

        self._frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

    def _update_image(self) -> None:
        self._image = self._IMAGES[self._frames_counter.current_index]
        self._frames_counter.next()

    def _handle_collision_with_player(self) -> None:
        if not self._map.player.has_shield:
            self._to_delete = True
            self._map.player.add_shield()
            shield_sound.play()
