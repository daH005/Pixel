from pygame import Surface, Rect
from abc import ABC

from engine.common.colors import Color
from engine.abstract_ui import AbstractUI
from engine.scenes.abstract_scene import AbstractScene
from engine.scenes.manager import ScenesManager
from game.assets.images import BackgroundImages
from game.assets.sounds import level_ending_music
from game.scenes.keys import SceneKey

__all__ = (
    'AbstractLevelOverlayScene',
    'AbstractLevelEndingScene',
    'HomeBackground',
)


class AbstractLevelOverlayScene(AbstractScene, ABC):
    _background_image: Surface

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)
        self._init_overlay()

    def _init_overlay(self) -> None:
        self._overlay_image: Surface = Surface(self._screen.get_size())
        self._overlay_image.fill(Color.BLACK)
        self._overlay_image.set_alpha(100)

    def on_open(self) -> None:
        self._background_image = self._scenes_manager.get(SceneKey.LEVEL).saved_screen
        self._background_image.blit(self._overlay_image, (0, 0))

    def update(self) -> None:
        super().update()
        self._screen.blit(self._background_image, (0, 0))


class AbstractLevelEndingScene(AbstractLevelOverlayScene, ABC):

    def on_open(self) -> None:
        super().on_open()
        level_ending_music.play(-1)

    def on_close(self) -> None:
        level_ending_music.stop()


class HomeBackground(AbstractUI):

    def __init__(self) -> None:
        super().__init__(rect=BackgroundImages.HOME.get_rect())
        self._image: Surface = BackgroundImages.HOME.copy()

        borders_rect: Rect = BackgroundImages.TOP_HOME_BORDER.get_rect(centerx=self._screen.get_width() // 2)
        self._image.blit(BackgroundImages.TOP_HOME_BORDER, borders_rect)

        borders_rect.bottom = self._screen.get_height()
        self._image.blit(BackgroundImages.BOTTOM_HOME_BORDER, borders_rect)
