from random import uniform, randint

from engine.abstract_ui import AbstractUI
from engine.map_.camera import Camera
from engine.map_.map_ import Map
from engine.common.counters import TimeCounter
from engine.common.float_rect import FloatRect
from engine.common.colors import Color
from game.assets.fonts import PixelFonts
from game.assets.images import (
    BackgroundImages,
    CLOUDS_IMAGES,
    COIN_IMAGES,
    HEART_IMAGES,
    SHIELD_IMAGES,
)
from game.assets.save import get_coins_count
from game.map_.ui.coin import Coin

__all__ = (
    'Background',
    'CloudsManager',
    'CoinsCounterHUD',
    'PlayerHPHUD',
)


class Background(AbstractUI):

    def __init__(self, camera: Camera) -> None:
        super().__init__()
        self._camera = camera

        self._image = BackgroundImages.MAP
        self._w: int = self._image.get_width()
        self._h: int = self._image.get_height()
        self._y = self._screen.get_height() - self._h
        self._smooth: float = 0.03
        self._float_x: float = 0

    def update(self) -> None:
        self._update_float_x()
        self._draw()
        self._draw(1)

    def _update_float_x(self) -> None:
        self._float_x = -self._camera.float_x * self._smooth

    def _draw(self, right_x_indent_factor: int = 0) -> None:
        x = round(self._float_x) + right_x_indent_factor * self._w
        self._screen.blit(self._image, (x, self._y))


class CloudsManager:

    def __init__(self) -> None:
        self._initial_clouds_count: int = 50
        self._clouds: list[Cloud] = []
        self._spawn_delay_timer: TimeCounter = TimeCounter(20)

    def reset(self) -> None:
        self._clouds.clear()
        self._create_initial_clouds()

    def _create_initial_clouds(self) -> None:
        for i in range(self._initial_clouds_count):
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


class Cloud(AbstractUI):
    _AREA_H: int = 300
    _RANDOM_SPEED_RANGE: tuple[float, float] = (0, 0.05)

    def __init__(self, x: int, y: int,
                 image_variant_index: int,
                 x_vel: float = 1,
                 ) -> None:
        super().__init__()
        self._x_vel: float = x_vel
        self._image = CLOUDS_IMAGES[image_variant_index]
        self._rect: FloatRect = FloatRect((x, y) + self._image.get_size())
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
            image_variant_index=randint(0, len(CLOUDS_IMAGES) - 1),
            x_vel=uniform(*cls._RANDOM_SPEED_RANGE),
        )
        if behind_left_edge:
            cloud._rect.right = 0
            cloud.float_x = cloud._rect.x
        return cloud

    def update(self) -> None:
        self._rect.float_x += self._x_vel
        if self._rect.left > self._screen.get_width():
            self._to_delete = True
        super().update()


class CoinsCounterHUD(AbstractUI):

    def __init__(self) -> None:
        self._image = COIN_IMAGES[0].copy()
        super().__init__(rect=self._image.get_rect(topright=self._screen.get_rect().topright))

    def update(self) -> None:
        super().update()
        self._update_count_surface()

    def _update_count_surface(self) -> None:
        count_text: str = str(get_coins_count() + Coin.visual_collected_count)  # type: ignore
        count_surface = PixelFonts.SMALL.render(
            count_text, 0,
            Color.WHITE,
        )
        self._screen.blit(count_surface, count_surface.get_rect(midright=self._rect.midleft))


class PlayerHPHUD(AbstractUI):

    def __init__(self, map_: Map) -> None:
        super().__init__()
        self._map = map_

        self._heart_image = HEART_IMAGES[0]
        self._lost_heart_image = self._heart_image.copy()
        self._lost_heart_image.set_alpha(100)
        self._shield_image = SHIELD_IMAGES[-2]
        self._w: int = self._heart_image.get_width()

    def _draw(self) -> None:
        cur_x: int = 0
        for i in range(self._map.player.max_hp):
            if i + 1 <= self._map.player.hp:
                self._screen.blit(self._heart_image, (cur_x, 0))
            else:
                self._screen.blit(self._lost_heart_image, (cur_x, 0))
            cur_x += self._w
        if self._map.player.has_shield:
            self._screen.blit(self._shield_image, (cur_x, 0))
