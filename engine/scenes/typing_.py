from typing import TypeAlias, TypeVar

from engine.scenes.abstract_scene import AbstractScene

__all__ = (
    'SceneKeyType',
    'AnySceneType',
)

SceneKeyType: TypeAlias = int
AnySceneType: TypeVar = TypeVar('AnySceneType', bound=AbstractScene)
