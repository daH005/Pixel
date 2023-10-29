from __future__ import annotations
from pygame import KEYDOWN, K_ESCAPE
from pygame.event import Event

from game.contrib.colors import Color
from game.contrib.windows import AbstractButton
from game.scenes.base import ScenesManager, AbstractScene, SceneKey
from game.contrib.screen import SCREEN_RECT
from game.scenes.common_ui import RestartButton, LevelsMenuButton, ButtonMixin, LevelOverlayBackground


__all__ = (
    'LevelPauseScene',
)


@ScenesManager.add(SceneKey.LEVEL_PAUSE)
class LevelPauseScene(AbstractScene):
    """Меню паузы, переход на которое осуществляется с `PlayScene`."""

    Background = LevelOverlayBackground

    class ButtonMixin(ButtonMixin):
        TOP_AND_BOTTOM_Y_INDENT: int = 10

    class ContinueButton(ButtonMixin, AbstractButton):
        text: str = 'Продолжить'
        HOVER_BACKGROUND_COLOR: Color = Color.GREEN

        def __init__(self, bottom_y: int) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = bottom_y - self.TOP_AND_BOTTOM_Y_INDENT

        def on_click(self) -> None:
            ScenesManager.switch(SceneKey.LEVEL)

    class RestartButton(RestartButton):

        def __init__(self) -> None:
            super().__init__()
            self.rect.centery = SCREEN_RECT.centery

    class LevelsMenuButton(ButtonMixin, LevelsMenuButton):

        def __init__(self, top_y: int) -> None:
            super().__init__()
            self.rect.top = top_y + self.TOP_AND_BOTTOM_Y_INDENT

    def __init__(self) -> None:
        self.background = self.Background()
        self.restart_button = self.RestartButton()
        self.levels_menu_button = self.LevelsMenuButton(self.restart_button.rect.bottom)
        self.continue_button = self.ContinueButton(self.restart_button.rect.top)

    def _handle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ScenesManager.switch(SceneKey.LEVEL)

    def _update(self) -> None:
        self.background.update()
        self.continue_button.update()
        self.levels_menu_button.update()
        self.restart_button.update()
