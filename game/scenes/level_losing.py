from __future__ import annotations

from game.contrib.screen import screen
from game.contrib.colors import Color
from game.contrib.windows import AbstractTextWindow
from game.scenes.base import ScenesManager, SceneKey
from game.contrib.screen import SCREEN_RECT
from game.scenes.common_ui import (
    RestartButton,
    LevelsMenuButton,
    LevelOverlayBackground,
    AbstractLevelEndingScene,
)

__all__ = (
    'LevelLosingScene',
)


@ScenesManager.add(SceneKey.LEVEL_LOSING)
class LevelLosingScene(AbstractLevelEndingScene):
    """Сцена, появляющаяся при смерти игрока.
    Большая часть реализации взята из `PlayPauseScene`.
    """

    Background = LevelOverlayBackground

    class LosingWindow(AbstractTextWindow):
        text: str = 'Вы погибли!'
        W: int = 400
        INNER_INDENT: int = 40
        DEFAULT_TEXT_COLOR: Color = Color.RED
        BOTTOM_Y_INDENT: int = 20

        def __init__(self, bottom_y: int) -> None:
            super().__init__()
            self.rect.centerx = screen.get_rect().centerx
            self.rect.bottom = bottom_y - self.BOTTOM_Y_INDENT

    class ButtonMixin:
        TOP_AND_BUTTON_Y_INDENT: int = 5

    class RestartButton(ButtonMixin, RestartButton):

        def __init__(self) -> None:
            super().__init__()
            self.rect.bottom = SCREEN_RECT.centery - self.TOP_AND_BUTTON_Y_INDENT

    class LevelsMenuButton(ButtonMixin, LevelsMenuButton):

        def __init__(self) -> None:
            super().__init__()
            self.rect.top = SCREEN_RECT.centery + self.TOP_AND_BUTTON_Y_INDENT

    def __init__(self) -> None:
        self.background = self.Background()
        self.restart_button = self.RestartButton()
        self.levels_menu_button = self.LevelsMenuButton()
        self.losing_window = self.LosingWindow(self.restart_button.rect.top)

    def _update(self) -> None:
        self.background.update()
        self.losing_window.update()
        self.restart_button.update()
        self.levels_menu_button.update()
