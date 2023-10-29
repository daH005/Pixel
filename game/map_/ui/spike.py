from pygame import Surface

from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.map_.map_ import Map
from game.contrib.annotations import SizeTupleType
from game.assets.images import SPIKE_IMAGE

__all__ = (
    'Spike',
)


@Map.add_object_type
class Spike(AbstractInteractingWithPlayerMapObject):
    image: Surface = SPIKE_IMAGE
    size: SizeTupleType = image.get_size()
    Z_INDEX: int = 1
    PLAYER_Y_VEL_FOR_HITTING: float = 5

    def _handle_collision_with_player(self) -> None:
        if self.map.player.y_vel >= self.PLAYER_Y_VEL_FOR_HITTING:
            self.map.player.hit()
