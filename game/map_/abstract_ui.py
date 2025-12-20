from abc import ABC, abstractmethod
from pygame import Rect

from engine.common.float_rect import FloatRect
from engine.map_.abstract_map_object import AbstractMapObject as BaseAbstractMapObject
from engine.map_.map_ import Map
from engine.exceptions import MapObjectCannotBeCreated
from game.map_.grid_attrs import GridObjectAttr
from game.map_.levels_extra_data_keys import LevelExtraDataKey

__all__ = (
    'AbstractMapObject',
    'AbstractBlock',
    'AbstractBackground',
    'AbstractInteractingWithPlayerMapObject',
    'AbstractItemToDisposableCollect',
    'AbstractMovingMapObject',
    'AbstractMovingAndInteractingWithPlayerMapObject',
    'AbstractXPatrolEnemy',
)


class AbstractMapObject(BaseAbstractMapObject):
    _map: 'ActualMapType'


class AbstractBlock(AbstractMapObject, ABC):

    _Z_INDEX = 10
    _GRID_ATTRS = [GridObjectAttr.BLOCK]


class AbstractBackground(AbstractMapObject, ABC):
    _Z_INDEX = -10


class AbstractInteractingWithPlayerMapObject(AbstractMapObject, ABC):

    def update(self) -> None:
        self._check_collision_with_player()
        super().update()

    def _check_collision_with_player(self) -> None:
        if self._rect.colliderect(self._map.player.get_rect()):
            self._handle_collision_with_player()

    @abstractmethod
    def _handle_collision_with_player(self) -> None:
        pass


class AbstractItemToDisposableCollect(AbstractInteractingWithPlayerMapObject, ABC):
    _collected_ids: list[int] = []

    def __init__(self, map_: Map,
                 rect: Rect | FloatRect,
                 id_: int | None = None,
                 ) -> None:
        if id_ in map_.levels_manager.current_level.extra.get(LevelExtraDataKey.COLLECTED_ITEMS_IDS, []):
            raise MapObjectCannotBeCreated

        super().__init__(
            map_=map_,
            rect=rect,
        )
        self._id = id_

    @classmethod
    def reset_class(cls) -> None:
        cls._collected_ids.clear()

    @classmethod
    @property
    def collected_ids(cls) -> list[int]:
        return cls._collected_ids

    def take(self) -> None:
        if self._id is None:
            return
        type(self)._collected_ids.append(self._id)


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
    _Z_INDEX = 5

    def update(self) -> None:
        self._move()
        AbstractInteractingWithPlayerMapObject.update(self)


class AbstractXPatrolEnemy(AbstractMovingAndInteractingWithPlayerMapObject, ABC):

    _SPEED: float = 1
    _X_PUSHING_POWER: float = 22
    _Y_PUSHING_POWER: float = 11

    def __init__(self, map_: Map,
                 rect: FloatRect,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=rect,
        )
        self._start_x = start_x
        self._end_x = end_x
        self._x_vel: float = self._SPEED

    def _move(self) -> None:
        if self._rect.left <= self._start_x or self._rect.right >= self._end_x:
            self._x_vel *= -1
        self._rect.float_x += self._x_vel

    def _handle_collision_with_player(self) -> None:
        self._map.player.hit(
            x_pushing=self._X_PUSHING_POWER,
            y_pushing=self._Y_PUSHING_POWER,
            enemy_center_x=self._rect.centerx,
        )


from game.map_ import Map as ActualMapType
