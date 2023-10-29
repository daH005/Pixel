"""Модуль располагает базовым функционалом для реализации сцен:
   - Менеджер сцен `ScenesManager` - класс-одиночка, служащий для хранения, передачи
   и переключения сцен;
   - Абстрактный класс сцены `AbstractScene`;
   - Перечисление ключей сцен для работы с ними через `ScenesManager`.
"""

from __future__ import annotations
from pygame import QUIT, Surface, Rect, KEYUP, K_f
from pygame.time import Clock
from pygame.event import get as get_events, Event
from typing import TypeVar, Callable, TypeAlias
from abc import ABC, abstractmethod
from enum import IntEnum

from game.contrib.colors import Color
from game.contrib.screen import screen
from game.assets.fonts import PIXEL_FONTS, FontSize
from game.contrib.singleton_ import SingletonMeta, SingletonABCMeta
from game.contrib.exceptions import Exit
from game.config import GameConfig

__all__ = (
    'clock',
    'SceneKey',
    'SceneKeyType',
    'ScenesManager',
    'AbstractScene',
    'SomeSceneType',
)

clock: Clock = Clock()


class SceneKey(IntEnum):
    HOME = 0
    LEVELS_MENU = 1
    LEVEL = 2
    LEVEL_PAUSE = 3
    LEVEL_LOSING = 4
    LEVEL_COMPLETION = 5


# Допускается возможность вместо `ScenesKey` использовать число.
SceneKeyType: TypeAlias = SceneKey | int


class ScenesManager(metaclass=SingletonMeta):
    SCENES: dict[SceneKeyType, SomeSceneType] = {}
    current_scene: SomeSceneType

    @classmethod
    def add(cls, new_scene_key: SceneKeyType) -> Callable[[type[SomeSceneType]], type[SomeSceneType]]:
        def wrapper(new_scene_type: type[SomeSceneType]) -> type[SomeSceneType]:
            cls.SCENES[new_scene_key] = new_scene_type()
            return new_scene_type
        return wrapper

    @classmethod
    def get(cls, scene_key: SceneKeyType) -> SomeSceneType:
        return cls.SCENES[scene_key]

    @classmethod
    def switch(cls, scene_to_switch_key: SceneKeyType) -> SomeSceneType:
        try:
            cls.current_scene.on_leave()
        except AttributeError:
            pass
        cls.current_scene = cls.SCENES[scene_to_switch_key]
        cls.current_scene.on_switch()
        return cls.current_scene


class AbstractScene(ABC, metaclass=SingletonABCMeta):

    def on_switch(self) -> None:
        """Вызывается при каждом переключении на сцену."""
        pass

    def on_leave(self) -> None:
        """Вызывается при каждом переключении с этой сцены на другую."""
        pass

    def reset(self, *args, **kwargs) -> None:
        """Даёт возможность обновлять заданные свойства сцены по необходимости."""
        pass

    def update(self) -> None:
        clock.tick(GameConfig.MAX_FPS)
        self._handle_events()
        self._update()
        self._show_fps()

    @staticmethod
    def _show_fps() -> None:
        fps_text: str = str(int(clock.get_fps()))
        fps_surface: Surface = PIXEL_FONTS[FontSize.SMALL].render(
            fps_text, 0,
            Color.WHITE,
        )
        fps_surface_rect: Rect = fps_surface.get_rect()
        fps_surface_rect.bottomright = screen.get_rect().bottomright
        screen.blit(fps_surface, fps_surface_rect)

    @abstractmethod
    def _update(self) -> None:
        pass

    def _handle_events(self) -> None:
        for event in get_events():
            if event.type == QUIT:
                raise Exit
            # Тестовый функционал:
            if event.type == KEYUP:
                if event.key == K_f:
                    if GameConfig.MAX_FPS == 60:
                        GameConfig.MAX_FPS = 5
                    elif GameConfig.MAX_FPS == 5:
                        GameConfig.MAX_FPS = 6000
                    elif GameConfig.MAX_FPS == 6000:
                        GameConfig.MAX_FPS = 60

            self._handle_event(event)

    def _handle_event(self, event: Event) -> None:
        pass


SomeSceneType: TypeVar = TypeVar('SomeSceneType', bound=AbstractScene, covariant=True)
