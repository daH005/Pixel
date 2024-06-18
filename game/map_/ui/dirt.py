from pygame import Surface

from engine.common.direction import Direction
from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractBlock, AbstractBackground
from game.assets.images import DirtImages

__all__ = (
    'Dirt',
    'BackgroundDirt',
)


@Map.add_object_type
class Dirt(AbstractBlock):
    _current_grass_index: int = 0

    _EDGES_IMAGES: dict[Direction, Surface] = {
        Direction.LEFT: DirtImages.LEFT,
        Direction.RIGHT: DirtImages.RIGHT,
    }

    def __init__(self, map_: Map,
                 x: int, y: int,
                 direction: Direction | None = None,
                 grass_enabled: bool = False,
                 ) -> None:
        self._direction = direction
        self._grass_enabled = grass_enabled
        self._init_image()
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _init_image(self) -> None:
        self._image: Surface
        if self._direction is not None:
            self._image = self._EDGES_IMAGES[self._direction].copy()
        else:
            self._image = DirtImages.DEFAULT.copy()
        if self._grass_enabled:
            self._image.blit(DirtImages.GRASS_LIST[self._current_grass_index], (0, 0))
            self._increment_grass_index()

    @classmethod
    def reset_class(cls) -> None:
        cls._current_grass_index = 0

    @classmethod
    def _increment_grass_index(cls) -> None:
        cls._current_grass_index += 1
        if cls._current_grass_index > len(DirtImages.GRASS_LIST) - 1:
            cls._current_grass_index = 0


@Map.add_object_type
class BackgroundDirt(AbstractBackground):

    def __init__(self, map_: Map, x: int, y: int) -> None:
        self._image = DirtImages.BACKGROUND
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )
