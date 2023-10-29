"""Общий для большинства сцен UI-функционал."""

from pygame import Surface
from abc import ABC

from game.scenes.base import ScenesManager, SceneKey, AbstractScene
from game.contrib.windows import AbstractButton
from game.contrib.colors import Color
from game.contrib.screen import SCREEN_RECT, SCREEN_SIZE, SCREEN_H, screen
from game.contrib.annotations import XYTupleType
from game.contrib.abstract_ui import AbstractUI
from game.assets.images import BackgroundImages
from game.assets.sounds import level_ending_music

__all__ = (
    'AbstractLevelEndingScene',
    'HomeBackground',
    'LevelOverlayBackground',
    'ButtonMixin',
    'RestartButton',
    'LevelsMenuButton',
)


class AbstractLevelEndingScene(AbstractScene, ABC):

    def on_switch(self) -> None:
        level_ending_music.play(-1)

    def on_leave(self) -> None:
        level_ending_music.stop()


class HomeBackground(AbstractUI):
    image: Surface = BackgroundImages.HOME
    rect: XYTupleType = (0, 0)
    BORDER_H: int = BackgroundImages.BOTTOM_HOME_BORDER.get_height()
    BORDER_X: int = SCREEN_RECT.centerx - BackgroundImages.BOTTOM_HOME_BORDER.get_width() // 2

    def update(self) -> None:
        super().update()
        screen.blit(BackgroundImages.TOP_HOME_BORDER, (self.BORDER_X, 0))
        screen.blit(BackgroundImages.BOTTOM_HOME_BORDER, (self.BORDER_X, SCREEN_H - self.BORDER_H))


class LevelOverlayBackground(AbstractUI):
    image: Surface
    rect: XYTupleType = (0, 0)
    ALPHA: int = 100

    def __init__(self) -> None:
        self.overlay_image: Surface = Surface(SCREEN_SIZE)
        self.overlay_image.fill(Color.BLACK)
        self.overlay_image.set_alpha(self.ALPHA)

    def _draw(self) -> None:
        screen.blit(ScenesManager.get(SceneKey.LEVEL).saved_screen, self.rect)
        screen.blit(self.overlay_image, self.rect)


class ButtonMixin:
    W: int = 300


class RestartButton(ButtonMixin, AbstractButton):
    text: str = 'Переиграть'
    HOVER_BACKGROUND_COLOR: Color = Color.GOLD

    def __init__(self) -> None:
        super().__init__()
        self.rect.centerx = SCREEN_RECT.centerx

    def on_click(self) -> None:
        ScenesManager.switch(SceneKey.LEVEL).reset()


class LevelsMenuButton(ButtonMixin, AbstractButton):
    text: str = 'В меню'

    def __init__(self) -> None:
        super().__init__()
        self.rect.centerx = SCREEN_RECT.centerx

    def on_click(self) -> None:
        ScenesManager.switch(SceneKey.LEVELS_MENU)
