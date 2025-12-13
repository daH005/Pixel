from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import LADDER_IMAGE

__all__ = (
    'Ladder',
)


@Map.add_object_type
class Ladder(AbstractInteractingWithPlayerMapObject):
    _image = LADDER_IMAGE

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _handle_collision_with_player(self) -> None:
        self._map.player.set_that_on_ladder()
