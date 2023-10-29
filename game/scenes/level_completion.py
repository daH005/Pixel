from __future__ import annotations

from game.contrib.colors import Color
from game.contrib.windows import AbstractTextWindow, AbstractButton
from game.scenes.base import ScenesManager, SceneKey
from game.contrib.screen import SCREEN_RECT
from game.scenes.common_ui import (
    LevelsMenuButton,
    LevelOverlayBackground,
    ButtonMixin,
    AbstractLevelEndingScene,
)
from game.assets.levels import LevelsManager

__all__ = (
    'LevelCompletionScene',
)


@ScenesManager.add(SceneKey.LEVEL_COMPLETION)
class LevelCompletionScene(AbstractLevelEndingScene):
    """Сцена, появляющаяся при успешном прохождении уровня.
    Позволяет перейти либо на следующий уровень либо в меню.
    """

    Background = LevelOverlayBackground

    class CongWindow(AbstractTextWindow):
        text: str = 'Уровень пройден!'
        W: int = 400
        INNER_INDENT: int = 40
        DEFAULT_TEXT_COLOR: Color = Color.GREEN
        BOTTOM_Y_INDENT: int = 20

        def __init__(self, bottom_y: int) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = bottom_y - self.BOTTOM_Y_INDENT

    class ButtonMixin(ButtonMixin):
        TOP_AND_BOTTOM_Y_INDENT: int = 5

    class NextLevelButton(ButtonMixin, AbstractButton):
        text: str = 'Следующий'
        HOVER_BACKGROUND_COLOR: Color = Color.GREEN

        def __init__(self) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = SCREEN_RECT.centery - self.TOP_AND_BOTTOM_Y_INDENT

        def on_click(self) -> None:
            LevelsManager.go_next()
            ScenesManager.switch(SceneKey.LEVEL).reset()

    class LevelsMenuButton(ButtonMixin, LevelsMenuButton):

        def __init__(self) -> None:
            super().__init__()
            self.rect.top = SCREEN_RECT.centery + self.TOP_AND_BOTTOM_Y_INDENT

    def __init__(self) -> None:
        self.background = self.Background()
        self.next_level_button = self.NextLevelButton()
        self.levels_menu_button = self.LevelsMenuButton()
        self.cong_window = self.CongWindow(self.next_level_button.rect.top)

    def _update(self) -> None:
        self.background.update()
        self.cong_window.update()
        self.next_level_button.update()
        self.levels_menu_button.update()
