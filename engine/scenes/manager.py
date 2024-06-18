from typing import Callable

from engine.common.singleton import SingletonMeta
from engine.levels.manager import LevelsManager

__all__ = (
    'ScenesManager',
)


class ScenesManager(metaclass=SingletonMeta):

    _scenes_types: dict['SceneKeyType', type['AnySceneType']] = {}
    _scenes: dict['SceneKeyType', 'AnySceneType'] = {}
    _current_scene: 'AnySceneType' = None

    def __init__(self, initial_scene_key: 'SceneKeyType',
                 levels_manager: LevelsManager,
                 ) -> None:
        self._initial_scene_key = initial_scene_key
        self._levels_manager = levels_manager

    @property
    def levels_manager(self) -> LevelsManager:
        return self._levels_manager

    @property
    def current_scene(self) -> 'AnySceneType':
        return self._current_scene

    @classmethod
    def add(cls, new_scene_key: 'SceneKeyType') -> Callable[[type['AnySceneType']], type['AnySceneType']]:
        def wrapper(new_scene_type: type[AnySceneType]) -> type[AnySceneType]:
            cls._scenes_types[new_scene_key] = new_scene_type
            return new_scene_type
        return wrapper

    def init(self) -> None:
        for scene_key, scene_type in self._scenes_types.items():
            self._scenes[scene_key] = scene_type(scenes_manager=self)
        self.switch_to(self._initial_scene_key)

    def get(self, scene_key: 'SceneKeyType') -> 'AnySceneType':
        return self._scenes[scene_key]

    def switch_to(self, scene_to_switch_key: 'SceneKeyType') -> 'AnySceneType':
        if self._current_scene is not None:
            self._current_scene.on_close()
        self._current_scene = self._scenes[scene_to_switch_key]
        self._current_scene.on_open()
        return self._current_scene


from engine.scenes.typing_ import SceneKeyType, AnySceneType
