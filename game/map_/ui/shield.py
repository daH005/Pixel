from game.assets.images import SHIELD_IMAGES
from game.assets.sounds import shield_sound
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject

__all__ = (
    'Shield',
)


@Map.add_object_type
class Shield(AbstractInteractingWithPlayerMapObject):
    size: SizeTupleType = SHIELD_IMAGES[0].get_size()
    ANIM_DELAY: float = 0.1

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SHIELD_IMAGES),
            transition_delay_as_seconds=self.ANIM_DELAY,
        )

    def _update_image(self) -> None:
        self.image = SHIELD_IMAGES[self.frames_counter.current_index]
        self.frames_counter.next()

    def _handle_collision_with_player(self) -> None:
        if not self.map.player.has_shield:
            self.to_delete = True
            self.map.player.has_shield = True
            shield_sound.play()
