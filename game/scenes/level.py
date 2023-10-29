from __future__ import annotations
from pygame import Surface, KEYDOWN, K_ESCAPE
from pygame.event import Event
from random import uniform, randint

from game.contrib.screen import screen
from game.contrib.annotations import XYTupleType
from game.assets.images import (
    BackgroundImages,
    SUN_IMAGE,
    CLOUDS_IMAGES,
    COIN_IMAGES,
    HEART_IMAGES,
    SHIELD_IMAGES,
)
from game.assets.sounds import level_music
from game.assets.fonts import PIXEL_FONTS, FontSize
from game.assets.save import save
from game.contrib.colors import Color
from game.scenes.base import ScenesManager, AbstractScene, SceneKey
from game.contrib.screen import SCREEN_W, SCREEN_H
from game.map_ import Map
from game.contrib.abstract_ui import AbstractUI
from game.contrib.counters import TimeCounter
from game.contrib.rects import FloatRect

__all__ = (
    'LevelScene',
)


@ScenesManager.add(SceneKey.LEVEL)
class LevelScene(AbstractScene):
    """Сцена с уровнем.
    По задумке на фоне мы располагаем горы, солнце,
    а также регулярно спавним облака.
    Карта обрабатывается частично, благодаря реализованному
    механизму "чанков".
    Камера сделана плавной.
    """

    BACKGROUND_COLOR: Color = Color.BLUE
    _screen_saving_enabled: bool = False
    saved_screen: Surface

    class Background(AbstractUI):
        image: Surface = BackgroundImages.MAP
        IMAGE_W: int = image.get_width()
        IMAGE_H: int = image.get_height()
        SMOOTH: float = 0.03

        def __init__(self) -> None:
            self.map = Map()
            self.float_x: float = 0

        def update(self) -> None:
            self._update_float_x()
            self._draw()
            self._draw(self.IMAGE_W)

        def _update_float_x(self) -> None:
            self.float_x = -self.map.camera.rect.float_x * self.SMOOTH

        def _draw(self, right_x_indent: int = 0) -> None:
            screen.blit(self.image, (round(self.float_x) + right_x_indent, SCREEN_H - self.IMAGE_H))

    class Sun(AbstractUI):
        image: Surface = SUN_IMAGE
        rect: XYTupleType = (50, 50)

    class CloudsManager:
        SPAWN_ONCE_EVERY: float = 20
        INITIAL_CLOUDS_COUNT: int = 50

        def __init__(self) -> None:
            self.clouds: list[LevelScene.Cloud] = []
            self.spawn_timer: TimeCounter = TimeCounter(self.SPAWN_ONCE_EVERY)

        def reset(self) -> None:
            self.clouds.clear()
            self._create_initial_clouds()

        def _create_initial_clouds(self) -> None:
            for i in range(self.INITIAL_CLOUDS_COUNT):
                self.clouds.append(self._new_random_cloud(behind_left_edge=False))

        def update(self) -> None:
            self.spawn_timer.next()
            if not self.spawn_timer.is_work():
                self.clouds.append(self._new_random_cloud())
                self.spawn_timer.restart()
            for cloud in self.clouds[:]:
                cloud.update()
                if cloud.to_delete:
                    self.clouds.remove(cloud)

        @staticmethod
        def _new_random_cloud(behind_left_edge: bool = True) -> LevelScene.Cloud:
            return LevelScene.Cloud.new_random_cloud(behind_left_edge)

    class Cloud(AbstractUI):
        CLOUDS_AREA_H: int = 300
        RANDOM_SPEED_RANGE: tuple[float, float] = (0, 0.05)

        def __init__(self, x: int, y: int,
                     image_variant_index: int, x_vel: float = 1,
                     ) -> None:
            self.x_vel: float = x_vel
            self.image: Surface = CLOUDS_IMAGES[image_variant_index]
            self.rect: FloatRect = FloatRect((x, y) + self.image.get_size())
            self.to_delete: bool = False

        @classmethod
        def new_random_cloud(cls, behind_left_edge: bool = True) -> LevelScene.Cloud:
            x: int = 0
            if not behind_left_edge:
                x = randint(0, SCREEN_W)
            cloud: cls = cls(
                x=x,
                y=randint(0, cls.CLOUDS_AREA_H),
                image_variant_index=randint(0, len(CLOUDS_IMAGES) - 1),
                x_vel=uniform(*cls.RANDOM_SPEED_RANGE),
            )
            if behind_left_edge:
                cloud.rect.right = 0
                cloud.float_x = cloud.rect.x
            return cloud

        def update(self) -> None:
            self.rect.float_x += self.x_vel
            if self.rect.left > SCREEN_W:
                self.to_delete = True
            super().update()

    class CoinsCounterHUD(AbstractUI):
        image: Surface = COIN_IMAGES[0]
        rect: XYTupleType = (SCREEN_W - image.get_width(), 0)
        IMAGE_LEFT_X_INDENT: int = 10

        def update(self) -> None:
            super().update()
            self._update_count_surface()

        def _update_count_surface(self) -> None:
            count_text: str = str(self._full_count())
            count_surface: Surface = PIXEL_FONTS[FontSize.SMALL].render(
                count_text, 0,
                Color.WHITE,
            )
            screen.blit(count_surface, (
                self.rect[0] - self.IMAGE_LEFT_X_INDENT - count_surface.get_width(),
                self.rect[1] + count_surface.get_height() // 2,
            ))

        @staticmethod
        def _full_count() -> int:
            return save.coins_count + Map().visual_taken_coins_count

    class PlayerHpHUD(AbstractUI):
        image: Surface = HEART_IMAGES[0]
        LOST_HEART_IMAGE: Surface = image.copy()
        LOST_HEART_IMAGE.set_alpha(100)
        W: int = HEART_IMAGES[0].get_width()

        def _draw(self) -> None:
            cur_x: int = 0
            for i in range(Map().player.MAX_HP):
                if i + 1 <= Map().player.hp:
                    screen.blit(self.image, (cur_x, 0))
                else:
                    screen.blit(self.LOST_HEART_IMAGE, (cur_x, 0))
                cur_x += self.W
            if Map().player.has_shield:
                screen.blit(SHIELD_IMAGES[-2], (cur_x, 0))

    def __init__(self) -> None:
        self.map = Map()
        self.background = self.Background()
        self.sun = self.Sun()
        self.clouds = self.CloudsManager()
        self.coins_counter_hud = self.CoinsCounterHUD()
        self.player_hp_hud = self.PlayerHpHUD()

    def on_switch(self) -> None:
        self._screen_saving_enabled = False
        level_music.play(-1)

    def reset(self) -> None:
        self.map.reset()
        self.clouds.reset()

    def on_leave(self) -> None:
        level_music.stop()

    def _handle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ScenesManager.switch(SceneKey.LEVEL_PAUSE)
                self._screen_saving_enabled = True

    def _update(self) -> None:
        screen.fill(self.BACKGROUND_COLOR)
        self.sun.update()
        self.clouds.update()
        self.background.update()
        self.map.update()
        self._check_player_hp()
        self._check_level_completion()
        self._save_screen()
        self.player_hp_hud.update()
        self.coins_counter_hud.update()

    def _check_player_hp(self) -> None:
        if self.map.player.hp <= 0:
            ScenesManager.switch(SceneKey.LEVEL_LOSING)
            self._screen_saving_enabled = True

    def _check_level_completion(self) -> None:
        if self.map.is_completed:
            ScenesManager.switch(SceneKey.LEVEL_COMPLETION)
            self._screen_saving_enabled = True

    def _save_screen(self) -> None:
        if self._screen_saving_enabled:
            self.saved_screen = screen.copy()
