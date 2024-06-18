from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import FINISH_IMAGE

__all__ = (
    'Finish',
)


@Map.add_object_type
class Finish(AbstractInteractingWithPlayerMapObject):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        self._image = FINISH_IMAGE
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
            z_index=99,
        )

    def _handle_collision_with_player(self) -> None:
        self._map.finish()
