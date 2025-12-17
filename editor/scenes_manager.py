import json

import pygame as pg
from pygame.event import Event

from engine.common.direction import Direction
from engine.scenes.abstract_scene import AbstractScene
from engine.scenes.manager import ScenesManager
from game.assets.fonts import PixelFonts
from game.common.windows.windows import Button
from game.common.windows.building import TextWindowPartBuilder
from editor.types_ import *

__all__ = (
    'ScenesManager',
    'EditorScene',
)


@ScenesManager.add(0)
class EditorScene(AbstractScene):

    _BLOCK_SIZE: int = 40
    _OFFSET_SPEED: int = 10
    _RESULT_FILENAME: str = 'res.json'

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager)
        self._panel: _ObjectTypePanel = _ObjectTypePanel(self._object_type_panel_choice)
        self._panel_is_on: bool = False
        self._selected_object_type = Dirt
        self._selected_object_kwargs = {}

        self._delete_mode_is_on: bool = False
        self._objects: list[AbstractEditorObject] = []

        self._x_offset: int = 0
        self._y_offset: int = 0

    def _object_type_panel_choice(self, t, kwargs) -> None:
        self._selected_object_type = t
        self._selected_object_kwargs = kwargs

    def _handle_event(self, event: Event) -> None:
        super()._handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self._panel_is_on:
                    self._panel_is_on = False
                else:
                    self._panel_is_on = True
            elif event.key == pg.K_DELETE:
                if self._delete_mode_is_on:
                    self._delete_mode_is_on = False
                else:
                    self._delete_mode_is_on = True
            elif event.key == pg.K_SPACE:
                self._save_map()

    def update(self) -> None:
        super().update()

        self._screen.fill((255, 255, 255))
        self._handle_objects()
        self._handle_mouse()
        self._handle_presses()
        self._handle_panel()

    def _handle_mouse(self) -> None:
        if self._panel_is_on:
            return

        x_diff = self._x_offset % self._BLOCK_SIZE
        y_diff = self._y_offset % self._BLOCK_SIZE

        pos = pg.mouse.get_pos()
        block_x = pos[0] - (pos[0] + x_diff) % self._BLOCK_SIZE
        block_y = pos[1] - (pos[1] + y_diff) % self._BLOCK_SIZE
        pg.draw.rect(self._screen, (0, 0, 0), (block_x, block_y, self._BLOCK_SIZE, self._BLOCK_SIZE), width=1)

        if pg.mouse.get_pressed()[0]:
            if self._delete_mode_is_on:
                self._handle_deleting()
            else:
                self._handle_creating(block_x, block_y)

    def _handle_deleting(self) -> None:
        for ob in self._objects:
            if ob.get_rect().move(-self._x_offset, -self._y_offset).collidepoint(pg.mouse.get_pos()):
                self._objects.remove(ob)

    def _handle_creating(self, block_x: int, block_y: int) -> None:
        x = block_x + self._x_offset + self._BLOCK_SIZE // 2
        y = block_y + self._y_offset + self._BLOCK_SIZE
        ob = self._selected_object_type(x, y, **self._selected_object_kwargs)
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

    def _handle_panel(self) -> None:
        if self._panel_is_on:
            self._panel.update()

    def _save_map(self) -> None:
        m = {
            'objects': self._objects_to_json(),
            'is_available': True,
            'is_completed': False,
            'w': self._bigger_right_x(),
            'h': self._bigger_bottom_y(),
            'extra_data': {
                'ids': []
            },
            'camera_bounding_horizontal_lines': [],
        }

        with open(self._RESULT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(m, f)

    def _objects_to_json(self) -> list[dict]:
        obs = []
        for ob in self._objects:
            obs.append(ob.to_json())
        return obs

    def _bigger_right_x(self) -> int:
        bigger: int = 0
        for ob in self._objects:
            bigger = max(bigger, ob.get_rect().right)
        return bigger

    def _bigger_bottom_y(self) -> int:
        bigger: int = 0
        for ob in self._objects:
            bigger = max(bigger, ob.get_rect().bottom)
        return bigger


class _ObjectTypePanel:

    _TYPES_AND_ARGS = [
        (Dirt, dict()),
        (Dirt, dict(direction=Direction.LEFT)),
        (Dirt, dict(direction=Direction.RIGHT)),

        (Dirt, dict(grass_enabled=True)),
        (Dirt, dict(grass_enabled=True, direction=Direction.LEFT)),
        (Dirt, dict(grass_enabled=True, direction=Direction.RIGHT)),

        (Player, dict()),
        (Finish, dict()),
    ]

    def __init__(self, on_click) -> None:
        self._on_click = on_click
        self._buttons: list[Button] = []
        y: int = 0
        for t, kwargs in self._TYPES_AND_ARGS:
            button = self._new_button(t, kwargs, y)
            self._buttons.append(button)
            y += button.get_rect().h

    def _new_button(self, t, kwargs, y: int) -> Button:
        return Button(
            builder=TextWindowPartBuilder(
                text=t.__name__ + ' ' + str(kwargs),
                font=PixelFonts.VERY_SMALL,
                inner_indent=5,
                border_wh=2,
            ),
            x=0,
            y=y,
            on_click=lambda: self._on_click(t, kwargs),
        )

    def update(self) -> None:
        for button in self._buttons:
            button.update()
