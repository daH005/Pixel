from abc import ABC, abstractmethod
from pygame import Rect

from engine.common.float_rect import FloatRect
from engine.map_.grid.typing_ import AttrsType
from engine.map_.abstract_map_object import AbstractMapObject
from engine.map_.map_ import Map
from engine.exceptions import MapObjectCannotBeCreated
from game.map_.attrs import MapObjectAttr
from game.map_.levels_extra_data_keys import LevelExtraDataKey

__all__ = (
    'AbstractBlock',
    'AbstractBackground',
    'AbstractInteractingWithPlayerMapObject',
    'AbstractItemToDisposableCollect',
    'AbstractMovingMapObject',
    'AbstractMovingAndInteractingWithPlayerMapObject',
    'AbstractXPatrolEnemy',
)


class AbstractBlock(AbstractMapObject, ABC):

    def __init__(self, map_: Map,
                 rect: Rect | FloatRect,
                 z_index: int = 7,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=rect,
            attrs=[MapObjectAttr.BLOCK],
            z_index=z_index,
        )


class AbstractBackground(AbstractMapObject, ABC):

    def __init__(self, map_: Map,
                 rect: Rect | FloatRect,
                 z_index: int = -2,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=rect,
            z_index=z_index,
        )


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
                 attrs: AttrsType | None = None,
                 z_index: int = 1,
                 id_: int | None = None,
                 ) -> None:
        if id_ in map_.levels_manager.current_level.extra.get(LevelExtraDataKey.COLLECTED_ITEMS_IDS, []):
            raise MapObjectCannotBeCreated

        super().__init__(
            map_=map_,
            rect=rect,
            attrs=attrs,
            z_index=z_index,
        )
        self._id = id_

    @classmethod
    def reset_class(cls) -> None:
        AbstractItemToDisposableCollect._collected_ids.clear()

    @classmethod
    @property
    def collected_ids(cls) -> list[int]:
        return list(AbstractItemToDisposableCollect._collected_ids)

    def take(self) -> None:
        if self._id is None:
            return
        AbstractItemToDisposableCollect._collected_ids.append(self._id)


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

    def __init__(self, map_: Map,
                 rect: FloatRect,
                 start_x: int,
                 end_x: int,
                 speed: float,
                 attrs: AttrsType | None = None,
                 x_pushing_power: float = 22,
                 y_pushing_power: float = 11,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=rect,
            attrs=attrs,
            z_index=2,
        )
        self._start_x = start_x
        self._end_x = end_x
        self._speed = speed
        self._x_pushing_power = x_pushing_power
        self._y_pushing_power = y_pushing_power
        self._x_vel: float = self._speed

    def _move(self) -> None:
        if self._rect.left <= self._start_x or self._rect.right >= self._end_x:
            self._x_vel *= -1
        self._rect.float_x += self._x_vel

    def _handle_collision_with_player(self) -> None:
        self._map.player.hit(
            x_pushing=self._x_pushing_power,
            y_pushing=self._y_pushing_power,
            enemy_center_x=self._rect.centerx,
        )
