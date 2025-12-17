import pygame as pg

from engine.scenes.abstract_scene import AbstractScene
from engine.scenes.manager import ScenesManager
from editor.types_ import (
    AbstractEditorObject,
    Dirt,
)

__all__ = (
    'ScenesManager',
    'EditorScene',
)


@ScenesManager.add(0)
class EditorScene(AbstractScene):

    _BLOCK_SIZE: int = 40
    _OFFSET_SPEED: int = 10

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager)
        self._objects: list[AbstractEditorObject] = []
        self._selected_object_type = Dirt
        self._x_offset: int = 0
        self._y_offset: int = 0

    def update(self) -> None:
        super().update()

        self._screen.fill((255, 255, 255))
        self._handle_objects()
        self._handle_mouse()
        self._handle_presses()

    def _handle_mouse(self) -> None:
        x_diff = self._x_offset % self._BLOCK_SIZE
        y_diff = self._y_offset % self._BLOCK_SIZE

        pos = pg.mouse.get_pos()
        block_x = pos[0] - (pos[0] + x_diff) % self._BLOCK_SIZE
        block_y = pos[1] - (pos[1] + y_diff) % self._BLOCK_SIZE
        pg.draw.rect(self._screen, (0, 0, 0), (block_x, block_y, self._BLOCK_SIZE, self._BLOCK_SIZE), width=1)

        if pg.mouse.get_pressed()[0]:
            x = block_x + self._x_offset
            y = block_y + self._y_offset
            ob = self._selected_object_type(x, y)
            if ob not in self._objects:
                self._objects.append(ob)

    def _handle_presses(self) -> None:
        presses = pg.key.get_pressed()
        if presses[pg.K_RIGHT]:
            self._x_offset += self._OFFSET_SPEED
        elif presses[pg.K_LEFT]:
            self._x_offset -= self._OFFSET_SPEED
        elif presses[pg.K_DOWN]:
            self._y_offset += self._OFFSET_SPEED
        elif presses[pg.K_UP]:
            self._y_offset -= self._OFFSET_SPEED

        if self._x_offset < 0:
            self._x_offset = 0
        if self._y_offset < 0:
            self._y_offset = 0

    def _handle_objects(self) -> None:
        for ob in self._objects:
            ob.update(self._x_offset, self._y_offset)
