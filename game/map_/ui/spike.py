from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import SPIKE_IMAGE

__all__ = (
    'Spike',
)


@Map.add_object_type
class Spike(AbstractInteractingWithPlayerMapObject):
    _PLAYER_Y_VEL_FOR_HIT: float = 5

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        self._image = SPIKE_IMAGE
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _handle_collision_with_player(self) -> None:
        if self._map.player.y_vel >= self._PLAYER_Y_VEL_FOR_HIT:
            self._map.player.hit()
