from engine.common.direction import Direction
from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractBackground
from game.assets.images import WebImages

__all__ = (
    'Web',
)


@Map.add_object_type
class Web(AbstractBackground):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 direction: Direction,
                 ) -> None:
        self._image = WebImages.LEFT if direction == Direction.LEFT else WebImages.RIGHT
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )
