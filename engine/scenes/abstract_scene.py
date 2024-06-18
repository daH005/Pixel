from abc import ABC
from pygame import QUIT
from pygame.event import get as get_events, Event

from engine.common.singleton import SingletonABCMeta
from engine.screen_access_mixin import ScreenAccessMixin
from engine.exceptions import ExitFromGame

__all__ = (
    'AbstractScene',
)


class AbstractScene(ScreenAccessMixin, ABC, metaclass=SingletonABCMeta):

    def __init__(self, scenes_manager: 'ScenesManager') -> None:
        self._scenes_manager = scenes_manager

    def on_open(self) -> None:
        pass

    def on_close(self) -> None:
        pass

    def reset(self, *args, **kwargs) -> None:
        pass

    def update(self) -> None:
        self._handle_events()

    def _handle_events(self) -> None:
        for event in get_events():
            if event.type == QUIT:
                raise ExitFromGame
            self._handle_event(event)

    def _handle_event(self, event: Event) -> None:
        pass


from engine.scenes.manager import ScenesManager
