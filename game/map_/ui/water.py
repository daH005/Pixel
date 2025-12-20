from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import WaterImages

__all__ = (
    'Water',
)


@Map.add_object_type
class Water(AbstractInteractingWithPlayerMapObject):

    _Z_INDEX = 1
    _IMAGES = WaterImages

    def __init__(self, map_: Map,
                 x: int, y: int,
                 is_top: bool = False,
                 ):
        self._is_top = is_top
        self._init_image()
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _init_image(self) -> None:
        if self._is_top:
            self._image = self._IMAGES.TOP
        else:
            self._image = self._IMAGES.DEFAULT

    def _handle_collision_with_player(self) -> None:
        self._map.player.set_that_in_water()
