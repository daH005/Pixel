from abc import ABC, abstractmethod
from pygame import Rect

from game.contrib.annotations import XYTupleType
from game.contrib.rects import FloatRect
from game.map_.map_ import Map
from game.map_.grid import (
    AbstractMapGridObject,
    MapObjectAttr,
    MapObjectAttrsListType,
)
from game.map_.camera import Camera
from game.contrib.screen import screen

__all__ = (
    'AbstractMapObject',
    'AbstractMapObject',
    'AbstractBlock',
    'AbstractBackground',
    'AbstractInteractingWithPlayerMapObject',
    'AbstractMovingMapObject',
    'AbstractMovingAndInteractingWithPlayerMapObject',
    'AbstractXPatrolEnemy',
)


class AbstractMapObject(AbstractMapGridObject, ABC):
    Z_INDEX: int = 0
    ATTRS: MapObjectAttrsListType = []
    size: XYTupleType
    RectType: type[Rect] | type[FloatRect] = Rect

    def __init__(self, x: int, y: int) -> None:
        self.map: Map = Map()
        self.camera: Camera = Camera()
        self.rect: Rect | FloatRect = self.RectType((x, y) + self.size)
        self.to_delete: bool = False

    def update(self) -> None:
        self._update_image()
        super().update()

    def _update_image(self) -> None:
        pass

    def _draw(self) -> None:
        screen.blit(self.image, self.camera.apply(self.rect))


class AbstractBlock(AbstractMapObject, ABC):
    Z_INDEX: int = 7
    ATTRS: MapObjectAttrsListType = [MapObjectAttr.BLOCK]


class AbstractBackground(AbstractMapObject, ABC):
    Z_INDEX: int = -2


class AbstractInteractingWithPlayerMapObject(AbstractMapObject, ABC):

    def update(self) -> None:
        self._check_collision_with_player()
        super().update()

    def _check_collision_with_player(self) -> None:
        if self.rect.colliderect(self.map.player.rect):
            self._handle_collision_with_player()

    @abstractmethod
    def _handle_collision_with_player(self) -> None:
        pass


class AbstractMovingMapObject(AbstractMapObject, ABC):

    def update(self) -> None:
        self._move()
        super().update()

    @abstractmethod
    def _move(self) -> None:
        pass


class AbstractMovingAndInteractingWithPlayerMapObject(AbstractMovingMapObject,
                                                      AbstractInteractingWithPlayerMapObject,
                                                      ABC):

    def update(self) -> None:
        self._move()
        AbstractInteractingWithPlayerMapObject.update(self)


class AbstractXPatrolEnemy(AbstractMovingAndInteractingWithPlayerMapObject, ABC):
    Z_INDEX: int = 2
    RectType: type[FloatRect] = FloatRect
    X_PUSHING_POWER: float = 22
    Y_PUSHING_POWER: float = 11
    SPEED: float

    def __init__(self, x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(x, y)
        if start_x is None or end_x is None:
            raise ValueError(f'Диапазон патрулирования для моба {type(self).__name__} не указан!')
        self.start_x = start_x
        self.end_x = end_x
        self.x_vel: float = self.SPEED

    def _move(self) -> None:
        if self.rect.left <= self.start_x or self.rect.right >= self.end_x:
            self.x_vel *= -1
        self.rect.float_x += self.x_vel

    def _handle_collision_with_player(self) -> None:
        self.map.player.hit(
            x_pushing=self.X_PUSHING_POWER,
            y_pushing=self.Y_PUSHING_POWER,
            enemy_center_x=self.rect.centerx,
        )
