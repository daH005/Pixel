from random import uniform, randint
from typing import cast
from pygame import Surface, SRCALPHA

from engine.abstract_ui import AbstractNoSizeUI
from engine.map_.camera import Camera
from engine.common.counters import TimeCounter
from engine.common.colors import Color
from game.assets.fonts import PixelFonts
from game.assets.images import (
    BackgroundImages,
    CLOUDS_IMAGES,
    COIN_IMAGES,
    HEART_IMAGES,
    LOST_HEART_IMAGE,
    SHIELD_IMAGES,
)
from game.assets.save import get_coins_count
from game.map_.ui.coin import Coin
from game.map_.ui.player import Player
from game.map_ import Map

__all__ = (
    'Background',
    'CloudManager',
    'CoinCounterHUD',
    'PlayerHPHUD',
)


class Background(AbstractNoSizeUI):

    _image = BackgroundImages.MAP
    _SMOOTH: float = 0.03

    def __init__(self, camera: Camera) -> None:
        super().__init__(y=self._screen.get_height() - self._image.get_height())
        self._camera = camera
        self._float_x: float = 0

    def update(self) -> None:
        self._float_x = -self._camera.float_x * self._SMOOTH
        self._x = round(self._float_x)
        super().update()


class CloudManager:
    _INITIAL_CLOUDS_COUNT: int = 50

    def __init__(self) -> None:
        self._clouds: list[Cloud] = []
        self._spawn_delay_timer: TimeCounter = TimeCounter(20)

    def reset(self) -> None:
        self._clouds.clear()
        self._create_initial_clouds()

    def _create_initial_clouds(self) -> None:
        for i in range(self._INITIAL_CLOUDS_COUNT):
            self._clouds.append(self._new_random_cloud(behind_left_edge=False))

    def update(self) -> None:
        self._spawn_delay_timer.next()
        if not self._spawn_delay_timer.is_working():
            self._clouds.append(self._new_random_cloud())
            self._spawn_delay_timer.restart()
        for cloud in self._clouds[:]:
            cloud.update()
            if cloud.to_delete:
                self._clouds.remove(cloud)

    @staticmethod
    def _new_random_cloud(behind_left_edge: bool = True) -> 'Cloud':
        return Cloud.new_random_cloud(behind_left_edge)


class Cloud(AbstractNoSizeUI):

    _IMAGE_VARIANTS = CLOUDS_IMAGES
    _AREA_H: int = 300
    _RANDOM_SPEED_RANGE: tuple[float, float] = (0, 0.05)

    def __init__(self, x: int, y: int,
                 image_variant_index: int,
                 speed: float,
                 ) -> None:
        super().__init__(x, y)
        self._image = self._IMAGE_VARIANTS[image_variant_index]

        self._float_x: float = x
        self._x_vel: float = speed
        self._x_to_delete: int = self._screen.get_width()

        self._to_delete: bool = False

    @property
    def to_delete(self) -> bool:
        return self._to_delete

    @classmethod
    def new_random_cloud(cls, behind_left_edge: bool = True) -> 'Cloud':
        x: int = 0
        if not behind_left_edge:
            x = randint(0, cls._screen.get_width())  # noqa

        cloud: cls = cls(
            x=x,
            y=randint(0, cls._AREA_H),
            image_variant_index=randint(0, len(cls._IMAGE_VARIANTS) - 1),
            speed=uniform(*cls._RANDOM_SPEED_RANGE),
        )
        if behind_left_edge:
            cloud._float_x = -cloud._image.get_width()

        return cloud

    def update(self) -> None:
        self._float_x += self._x_vel
        self._x = int(self._float_x)
        if self._float_x > self._x_to_delete:
            self._to_delete = True
        super().update()


class CoinCounterHUD:

    def __init__(self) -> None:
        self._coin = _Coin()
        self._count = _Count(self._coin.x)

    def update(self) -> None:
        self._coin.update()
        self._count.update()


class _Coin(AbstractNoSizeUI):
    _image = COIN_IMAGES[0]

    def __init__(self) -> None:
        super().__init__(x=self._screen.get_width() - self._image.get_width(), y=0)


class _Count(AbstractNoSizeUI):

    def __init__(self, base_x: int) -> None:
        super().__init__()
        self._base_x = base_x
        self._count: int = -999

    def update(self) -> None:
        self._update_image()
        super().update()

    def _update_image(self) -> None:
        current_count: int = get_coins_count() + cast(int, Coin.visual_collected_count)
        if current_count == self._count:
            return

        self._image = PixelFonts.SMALL.render(
            str(current_count), 0,
            Color.WHITE,
        )
        self._x = self._base_x - self._image.get_width()


class PlayerHPHUD(AbstractNoSizeUI):

    _HEART_IMAGE = HEART_IMAGES[0]
    _LOST_HEART_IMAGE = LOST_HEART_IMAGE
    _SHIELD_IMAGE = SHIELD_IMAGES[-2]
    _HEART_W: int = _HEART_IMAGE.get_width()

    def __init__(self, map_: Map) -> None:
        super().__init__()
        self._map = map_

        self._hp: int = -999
        self._has_shield: bool | None = None
        self._w: int = cast(int, Player.max_hp) * self._HEART_W + self._SHIELD_IMAGE.get_width()
        self._h: int = self._HEART_IMAGE.get_height()

    def update(self) -> None:
        self._update_image()
        super().update()

    def _update_image(self) -> None:
        current_shield = self._map.player.has_shield
        current_hp = self._map.player.hp
        if current_shield == self._has_shield and current_hp == self._hp:
            return

        self._image = Surface((self._w, self._h), SRCALPHA)
        cur_x: int = 0
        for i in range(self._map.player.max_hp):
            if i + 1 <= self._map.player.hp:
                self._image.blit(self._HEART_IMAGE, (cur_x, 0))
            else:
                self._image.blit(self._LOST_HEART_IMAGE, (cur_x, 0))
            cur_x += self._HEART_W

        if self._map.player.has_shield:
            self._image.blit(self._SHIELD_IMAGE, (cur_x, 0))
