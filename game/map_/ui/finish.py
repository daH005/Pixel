from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import FINISH_IMAGE

__all__ = (
    'Finish',
)


@Map.add_object_type
class Finish(AbstractInteractingWithPlayerMapObject):
    _image = FINISH_IMAGE

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _on_collision_with_player(self) -> None:
        self._map.finish()
